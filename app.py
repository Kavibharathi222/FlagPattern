

# Import Necessary Libraries
import streamlit as st
import cv2
import numpy as np
from PIL import Image

#  Page title 
st.set_page_config(page_title="Flag Pattern Projection", page_icon="", layout="centered")

st.title("Mapping a Pattern onto a curved Surface")

# Project description 
st.sidebar.info("""
 About this Project

This tool demonstrates how to map a custom pattern or color onto a waving flag image,  
matching the folds and natural lighting for a realistic effect.

- Upload any pattern image (PNG/JPG)
- See how it wraps around the flag’s folds
- Download the final result

This is useful for:
- Visualizing custom flag designs
- Testing textures on fabric
- Learning image processing (OpenCV + Python)

---

Instructions:
1 Click **Browse files** to upload your pattern.  
2 Wait for the result to generate.  
3 Click **Download** to save the output.
""")



# Upload pattern image 
pattern_file = st.file_uploader(" Upload Pattern Image (JPG/PNG)", type=["jpg", "jpeg", "png"])

if pattern_file:
    # Load pattern image
    pattern_image = Image.open(pattern_file).convert("RGB")
    pattern = np.array(pattern_image)

    # Load the base flag image
    flag = cv2.imread("Flag.jpg")
    flag = cv2.cvtColor(flag, cv2.COLOR_BGR2RGB)

    # Manually defines the outline of the flag area you want to map the pattern onto.
    #These coordinates wrap the waving portion on the flag.
    polygon_points = np.array([
        (22, 25), (37, 25), (55, 29), (77, 31), (100, 37), (121, 44), (146, 44), (169, 43), (193, 43), (206, 36), (213, 53), (215, 65), (206, 76), (207, 87), (213, 96), (205, 111), (214, 129), (214, 146), (209, 165), (206, 180), (186, 176), (165, 180), (141, 172), (115, 166), (96, 156), (75, 153), (60, 152), (50, 158), (37, 161),
 (29, 162), (25, 148), (25, 130), (27, 103), (27, 69), (24, 48)
    ], np.int32).reshape((-1, 1, 2))
   

    #Creates a black mask.
    #Fills the polygon area with white (255)
    mask = np.zeros(flag.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [polygon_points], 255)
    
    #Finds the smallest rectangle that fits your polygon area.
    #Resizes the uploaded pattern to fit this area.  
    x, y, w, h = cv2.boundingRect(polygon_points)
    resized_pattern = cv2.resize(pattern, (w, h))

    #Creates a black canvas same size as the flag.
    #Handles cropping if the pattern exceeds the image bounds.
    pattern_canvas = np.zeros_like(flag)
    end_y = min(y + resized_pattern.shape[0], flag.shape[0])
    end_x = min(x + resized_pattern.shape[1], flag.shape[1])
    h_fit = end_y - y
    w_fit = end_x - x
    pattern_crop = resized_pattern[:h_fit, :w_fit]
    pattern_canvas[y:end_y, x:end_x] = pattern_crop

    #Converts the flag to grayscale to simulate lighting/shadow.
    #Normalizes it so darker areas get less pattern brightness, lighter areas get more.
    gray_flag = cv2.cvtColor(flag, cv2.COLOR_RGB2GRAY)
    light_map = cv2.normalize(gray_flag.astype("float32"), None, 0.4, 1.0, cv2.NORM_MINMAX)
    shaded_pattern = (pattern_canvas.astype("float32") * light_map[..., np.newaxis]).astype("uint8")
    
    #Uses the mask to get only the pattern + flag portion inside the polygon.
    #   Blends them: 80% pattern + 20% original flag → more realistic overlay
    pattern_region = cv2.bitwise_and(shaded_pattern, shaded_pattern, mask=mask)
    flag_region = cv2.bitwise_and(flag, flag, mask=mask)
    blended = cv2.addWeighted(pattern_region, 0.8, flag_region, 0.2, 0)

    #Keeps the unmasked part of the flag.
    #Adds the new blended region → final image with pattern only on the flag area.
    inv_mask = cv2.bitwise_not(mask)
    background = cv2.bitwise_and(flag, flag, mask=inv_mask)
    result = cv2.add(background, blended)

    #Displays the final realistic flag on your Streamlit page.
    st.image(result, caption=" Final Rendered Flag", use_column_width=True)

    result_bgr = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    is_success, buffer = cv2.imencode(".jpg", result_bgr)
    st.download_button(" Download Output", buffer.tobytes(), file_name="output.jpg", mime="image/jpeg")
