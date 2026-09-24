import tempfile

import streamlit as st

from core.pdf_checker import analyze_pdf
from core.parser import pdf_to_latex, pdf_to_markdown


st.set_page_config(
    page_title="Academic PDF Converter",
    layout="wide",
)

image_left, image_center, image_right = st.columns([1, 2, 1])
with image_center:
    st.image(
        "https://myresearchdata.blob.core.windows.net/academic/Academic_Dude.JPG",
        use_container_width=True,
    )
st.title("From Academic PDF to Editable Knowledge")
st.write(
    "Upload a research paper and turn it into clean, downloadable LaTeX and Markdown in seconds."
)

uploaded_file = st.file_uploader("Choose an Academic Paper PDF", type=["pdf"])

if uploaded_file and st.button("Convert"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.info("Analyzing PDF structure...")
    stats = analyze_pdf(tmp_path)
    st.write(f"Pages: {stats['page_count']} | Scanned: {stats['is_scanned']}")

    latex_output = pdf_to_latex(tmp_path)
    markdown_output = pdf_to_markdown(tmp_path)
    st.success("Conversion complete!")

    latex_column, markdown_column = st.columns([1, 1], gap="large")
    with latex_column:
        st.subheader("LaTeX (.tex)")
        st.code(latex_output, language="latex", height=600)
        st.download_button(
            "Download .tex",
            latex_output,
            file_name="converted.tex",
            mime="text/plain",
            use_container_width=True,
        )

    with markdown_column:
        st.subheader("Markdown (.md)")
        st.code(markdown_output, language="markdown", height=600)
        st.download_button(
            "Download .md",
            markdown_output,
            file_name="converted.md",
            mime="text/markdown",
            use_container_width=True,
        )

st.markdown(
    "<p style='text-align: center; font-style: italic;'>"
    "Are you thinking what I am thinking ? We both know what this tool will be used for !"
    "</p>",
    unsafe_allow_html=True,
)