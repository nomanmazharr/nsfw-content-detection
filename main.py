import streamlit as st
from nudenet import NudeDetector
from PIL import Image

# Initialize the detector
detector = NudeDetector()

# Serious labels for blocking nudity
block_labels = [
    "BUTTOCKS_EXPOSED",
    "FEMALE_BREAST_EXPOSED",
    "FEMALE_GENITALIA_EXPOSED",
    "ANUS_EXPOSED",
    "MALE_GENITALIA_EXPOSED",
    "BELLY_EXPOSED"
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

            # Save the uploaded image temporarily
            with open("temp_image.jpg", "wb") as f:
                f.write(uploaded_image.getbuffer())
            
            # Detect nudity
            results = detector.detect('temp_image.jpg')

            # Flag to block the image
            block_image = False

            # Check detection results
            for result in results:
                detected_class = result['class']  # Accessing the class key
                score = result['score'] * 100  # Assuming the score is from 0 to 1, converting to percentage

                # Block if serious class and score > 30%
                if detected_class in block_labels and score > 25:
                    block_image = True
                    st.error(f"Image blocked due to detected nudity: {detected_class} with score {score}%")
                    break
            
            if not block_image:
                st.success("The image does not include serious nudity.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
