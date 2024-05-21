import streamlit as st
from PIL import Image
import numpy as np

def embedding_image(main_image, watermark_image):
    # Ensure the watermark image has the same number of color channels as the main image
    if main_image.mode != watermark_image.mode:
        watermark_image = watermark_image.convert(main_image.mode)
    
    # Resize watermark to fit the main image
    wm_resized = watermark_image.resize((main_image.width, main_image.height), Image.LANCZOS)
    wm_array = np.array(wm_resized)
    main_array = np.array(main_image)
    
    # Embed the watermark into the main image
    for i in range(main_array.shape[0]):
        for j in range(main_array.shape[1]):
            for k in range(main_array.shape[2]):
                main_array[i, j, k] = (main_array[i, j, k] & 0xFE) | ((wm_array[i, j, k] >> 7) & 0x01)
    
    return Image.fromarray(main_array)

def extract_image(main_image):
    main_array = np.array(main_image)
    watermark_array = np.zeros_like(main_array)

    # Extract the watermark from the main image
    for i in range(main_array.shape[0]):
        for j in range(main_array.shape[1]):
            for k in range(main_array.shape[2]):
                watermark_array[i, j, k] = (main_array[i, j, k] & 0x01) * 255

    return Image.fromarray(watermark_array)

st.title("Digital Watermarking Tool")

option = st.selectbox("Choose an option", ["Watermark Embedding", "Watermark Extracting"])

if option == "Watermark Embedding":
    uploaded_main_file = st.file_uploader("Choose a main image...", type=["png", "jpg", "jpeg"])
    uploaded_watermark_file = st.file_uploader("Choose a watermark image...", type=["png", "jpg", "jpeg"])

    if uploaded_main_file is not None and uploaded_watermark_file is not None:
        main_image = Image.open(uploaded_main_file)
        watermark_image = Image.open(uploaded_watermark_file)
        
        if st.button('Embed Watermark'):
            watermarked_image = embedding_image(main_image, watermark_image)
            
            st.image(watermarked_image, caption='Watermarked Image', use_column_width=True)
            st.success('The digital watermark is inserted successfully!')

            # Save and provide download link
            watermarked_image.save('watermarked_image.png')
            with open("watermarked_image.png", "rb") as file:
                btn = st.download_button(
                    label="Download watermarked image",
                    data=file,
                    file_name="watermarked_image.png",
                    mime="image/png"
                )

elif option == "Watermark Extracting":
    uploaded_file = st.file_uploader("Choose an image to extract watermark...", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        main_image = Image.open(uploaded_file)
        
        if st.button('Extract Watermark'):
            extracted_watermark = extract_image(main_image)
            
            st.image(extracted_watermark, caption='Extracted Watermark', use_column_width=True)
            st.success('The digital watermark is extracted successfully!')

            # Save and provide download link
            extracted_watermark.save('extracted_watermark.png')
            with open("extracted_watermark.png", "rb") as file:
                btn = st.download_button(
                    label="Download extracted watermark image",
                    data=file,
                    file_name="extracted_watermark.png",
                    mime="image/png"
                )
