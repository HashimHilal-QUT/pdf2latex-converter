import streamlit as st
import tempfile
from core.pdf_checker import analyze_pdf

st.title("Academic PDF to LaTeX Converter")

input_type = st.radio("Input Method", ["Upload PDF", "DOI URL/ID"])

if input_type == "Upload PDF":
    uploaded_file = st.file_uploader("Choose an Academic Paper PDF", type=["pdf"])
    if uploaded_file and st.button("Convert to LaTeX"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        
        st.info("Analyzing PDF structure...")
        stats = analyze_pdf(tmp_path)
        st.write(f"Pages: {stats['page_count']} | Scanned: {stats['is_scanned']}")
        
        # Call your conversion pipeline here
        st.success("Conversion Complete!")
        st.code("\\documentclass{article}\n\\begin{document}\n...", language="latex")

elif input_type == "DOI URL/ID":
    doi_input = st.text_input("Enter DOI (e.g., 10.1145/3372278.3002678)")
    if doi_input and st.button("Fetch & Convert"):
        st.info(f"Searching metadata for DOI: {doi_input}...")