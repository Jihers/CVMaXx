
import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("OpenCV Test")

st.write("OpenCV version:", cv2.__version__)

uploaded_file = st.file_uploader(
    "Upload an X-ray or image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_array = np.array(image)

    st.subheader("Original Image")
    st.image(image_array, use_container_width=True)

    gray_image = cv2.cvtColor(
        image_array,
        cv2.COLOR_RGB2GRAY
    )

    st.subheader("Grayscale Image")
    st.image(gray_image, use_container_width=True)

    st.success("OpenCV is working correctly!")
