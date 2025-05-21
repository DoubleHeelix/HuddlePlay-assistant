import streamlit as st
from main import extract_text_from_image, suggest_reply, store_conversation

st.title("HuddlePlay Assistant")

# Upload screenshot
uploaded_file = st.file_uploader("Upload client screenshot", type=["png", "jpg", "jpeg"])

# Input draft message
user_draft = st.text_area("Enter your draft reply here:")

if uploaded_file and user_draft:
    # Save uploaded image temporarily
    with open("temp_screenshot.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract text from screenshot
    screenshot_text = extract_text_from_image("temp_screenshot.png")

    st.subheader("Extracted Client Message:")
    st.write(screenshot_text)

    # Generate suggestion
    suggested_reply = suggest_reply(screenshot_text, user_draft)

    st.subheader("Suggested Final Reply:")
    st.write(suggested_reply)

    # Optionally save conversation
    if st.button("Save Conversation"):
        store_conversation(screenshot_text, user_draft, suggested_reply)
        st.success("Conversation saved!")

else:
    st.info("Please upload a screenshot and enter your draft reply to get started.")
