# FlagPattern
This project demonstrates how to map a custom pattern or texture onto a waving flag image, simulating realistic folds and lighting using Python, OpenCV, NumPy, and Streamlit

# Dependencies
1. streamlit
2. opencv-python
3. numpy
4. Pillow

# Static Image

![Flag](https://github.com/user-attachments/assets/4ecf6aa6-5941-4484-bebc-374da8d353d4)

# Input Flag Given By User 

![Flag_of_England](https://github.com/user-attachments/assets/128dad4a-54ad-4f95-b9b8-0807ca488a23)

# Output Image 

![output (8)](https://github.com/user-attachments/assets/f17b673b-4d34-4431-8ba9-b62e83e38890)

# Features 
1. Upload any PNG/JPG pattern
2. Automatically maps the pattern to the flag area
3. Simulates realistic lighting using the flag’s folds
3. Download the final rendered flag image
4. Easy to run locally with Streamlit


# How it works 
1. Defines a polygon mask for the waving flag area
2. Resizes your pattern to fit inside the polygon
3. Uses the flag’s grayscale light map to shade the pattern
4. Blends the pattern + flag realistically
5. Lets you download the final image 


