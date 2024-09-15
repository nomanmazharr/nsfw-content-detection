import streamlit as st
from nudenet import NudeDetector
from PIL import Image

# Initialize the detector
detector = NudeDetector()

# Streamlit interface
st.title("Nudity Detection in Images")

# Upload image
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Display uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Button to check for nudity
    if st.button("Check for Nudity"):
        # Save the uploaded image temporarily
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_image.getbuffer())

        # Detect nudity
        results = detector.detect('temp_image.jpg')

        # Check if any nudity is detected
        if any(result['score'] > 0.5 for result in results):
            st.error("The image includes nudity.")
        else:
            st.success("The image does not include nudity.")
