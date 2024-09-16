import streamlit as st
from nudenet import NudeDetector
from PIL import Image
import numpy as np
import io

# Initialize the detector
detector = NudeDetector()

# Serious labels for blocking nudity (with a threshold of 30%)
block_labels_30 = [
    "BUTTOCKS_EXPOSED",
    "FEMALE_BREAST_EXPOSED",
    "FEMALE_GENITALIA_EXPOSED",
    "ANUS_EXPOSED",
    "MALE_GENITALIA_EXPOSED",
    "BELLY_EXPOSED"
]

# Labels with a higher threshold of 50%
block_labels_50 = [  
    "BUTTOCKS_COVERED",
    "FEMALE_BREAST_COVERED",
    "FEMALE_GENITALIA_COVERED",
    "ANUS_COVERED",
    "MALE_GENITALIA_COVERED"
]

# Streamlit interface
st.title("Nudity Detection in Images")

# Upload image
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    try:
        # Display uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Button to check for nudity
        if st.button("Check for Nudity"):
            st.write("Checking for nudity...")

            # Convert the image to a numpy array
            image_array = np.array(image)

            # Detect nudity
            results = detector.detect(image_array)

            # Flag to block the image
            block_image = False

            # Check detection results
            for result in results:
                detected_class = result['class']  # Accessing the class key
                score = result['score'] * 100  # Convert score to percentage

                # Block if serious nudity class with threshold of 30%
                if detected_class in block_labels_30 and score > 10:
                    block_image = True
                    st.error(f"Image blocked due to detected nudity: {detected_class} with score {score}%")
                    break

                # Add the belly-specific block with a higher threshold of 50%
                if detected_class in block_labels_50 and score > 50:
                    block_image = True
                    st.error(f"Image blocked due to detected nudity: {detected_class} with score {score}%")
                    break
            
            if not block_image:
                st.success("The image does not include serious nudity.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
