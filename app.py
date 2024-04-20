from dotenv import load_dotenv 
load_dotenv()      

import streamlit as st
import os
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
from PIL import Image
import tempfile

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image):
    if input != "":
        response = model.generate_content([input,image])
    else :
        response = model.generate_content(image)
    return response.text

st.set_page_config(page_title="Extract Content", page_icon="icon.png")
st.header("Automated Essay Analysis")

input = "Extract Handwritten text from PDF"

uploaded_file = st.file_uploader("Choose a PDF File...", type=["pdf"])

l = []

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file.seek(0)
        pdf_document = fitz.open(tmp_file.name)
        
        num_pages = len(pdf_document)
        
        for page_no in range(num_pages):
            page = pdf_document.load_page(page_no)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            st.image(img, caption=f"Page {page_no + 1}", use_column_width=True)
            response=get_gemini_response(input,img)
            st.subheader("The Response is ")
            l.append(response)
            st.write(response)

for x in l:
    print(x)