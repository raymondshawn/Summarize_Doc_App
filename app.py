import streamlit as st
from io import StringIO
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
import os
from langchain.chains.summarize import load_summarize_chain
from PyPDF2 import PdfReader
from docx import Document


def read_file(file):
    """Read file and return contents as a string"""

    file_ext = get_file_ext(file)

    if file_ext == "pdf":
        return read_pdf(file)
    elif file_ext == "docx":
        return read_docx(file)
    elif file_ext=="txt":
        return read_txt(file)


def get_file_ext(file):
    """Get file extension from filename"""
    return file.name.split(".")[-1]


def read_pdf(file):
    """Read PDF file and return text contents"""
    text = ""
    pdf = PdfReader(file)
    num_pages = len(pdf.pages)

    for i in range(num_pages):
        page = pdf.pages[i]
        content = page.extract_text()
        text += content

    return text


def read_docx(file):
    """Read DOCX file and return text contents"""
    document = Document(file)

    full_text = []
    for para in document.paragraphs:
        full_text.append(para.text)

    return '\n'.join(full_text)


def read_txt(file):
    """Read file of other format and return text contents"""
    stringio = StringIO(file.getvalue().decode("utf-8"))
    return stringio.read()


def create_documents(text):
    text_splitter = CharacterTextSplitter(
        chunk_size=100, chunk_overlap=20
    )

    documents = text_splitter.create_documents([text])
    return documents


def generate_summary(docs):
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    chain = load_summarize_chain(llm, chain_type="stuff")
    summary = chain.run(docs)
    return summary


st.title("🦜️🔗 Summarize  File")
st.text("Upload txt or docx or pdf file.You can upload multiple files")
uploaded_files = st.file_uploader("Choose a  txt file", accept_multiple_files=True)

with  st.form("Form"):
    api_key = st.text_area("Enter your OpenAI key:")

    submitted = st.form_submit_button("Submit")
    if submitted and api_key and uploaded_files:
        os.environ["OPENAI_API_KEY"] = api_key
        with st.spinner('Generating Summary...'):

            for file in uploaded_files:
                text = read_file(file)
                documents = create_documents(text)
                response = generate_summary(documents)

                if len(response):
                    st.write(f"summary for {file.name}")
                    st.info(response)
