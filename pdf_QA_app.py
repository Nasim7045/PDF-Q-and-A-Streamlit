import os
import google.generativeai as genai
import fitz  # PyMuPDF
import streamlit as st

# Hardcoded API key (Not recommended for production)
api_key = "set your api key here"  # Replace with your actual API key

# Check if the API key is valid
if not api_key:
    st.error("API key is missing. Please hardcode the API key in the script.")
else:
    # Configure Generative AI API
    genai.configure(api_key=api_key)

# Configure generation settings for the model
generation_config = {
    "temperature": 1.2,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the GenerativeModel with your configuration
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)
chat_session = model.start_chat(history=[])

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_document = fitz.open(stream=pdf_file, filetype="pdf")
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Streamlit UI
st.title("PDF Question-Answer Assistant")

# Upload PDF section
uploaded_pdf = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_pdf:
    try:
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(uploaded_pdf.read())
        st.success("PDF uploaded and text extracted successfully!")
        
        # Input for questions
        question = st.text_input("Enter your question about the PDF content:")

        if question:
            input_text = f"Here is the text from the PDF:\n\n{pdf_text}\n\nQuestion: {question}"
            response = chat_session.send_message(input_text)
            response_text = response.text

            # Display the response
            st.write("AI Response:", response_text)

            # Save the conversation history
            chat_session.history.append({"role": "user", "parts": [question]})
            chat_session.history.append({"role": "model", "parts": [response_text]})

    except Exception as e:
        st.error(f"An error occurred while processing the PDF: {e}")
