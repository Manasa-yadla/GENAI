import streamlit as st
import requests

# Streamlit app title
st.title("📚 Personalized Learning Assistant")

# User input for the question
user_question = st.text_input("Enter your question:")

# Dropdown for grade level selection
grade_level = st.selectbox(
    "Select your grade level:",
    ["Elementary", "Middle School", "High School", "College"]
)

# Button to submit the question
if st.button("Get Answer"):
    if user_question:
        with st.spinner("Thinking..."):
            try:
                # Send POST request to the Flask backend
                response = requests.post(
                    "http://localhost:5000/ask",
                    json={"question": user_question, "grade_level": grade_level.lower()}
                )
                result = response.json()
                if "answer" in result:
                    answer = result["answer"]
                    st.success("Answer:")
                    st.write(answer)
                elif "error" in result:
                    st.error(f"Error: {result['error']}")

            except Exception as e:
                # Display error message
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")

# Footer
st.markdown("---")
st.markdown("Developed by Manasa")
