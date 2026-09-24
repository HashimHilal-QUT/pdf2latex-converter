import streamlit as st

st.set_page_config(page_title="PDF2LaTeX Converter", page_icon="📄")
st.title("PDF2LaTeX Converter")
st.write("Upload a PDF to begin the conversion workflow.")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.success(f"Loaded: {uploaded_file.name}")
    st.info("The full conversion pipeline will be implemented here.")
