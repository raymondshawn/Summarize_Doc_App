import langchain
import streamlit as st
from io import StringIO
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
import os
from langchain.chains.summarize import load_summarize_chain


def read_file_as_string(file):


    # To convert to a string based IO:
    stringio = StringIO(file.getvalue().decode("utf-8"))

    # To read file as string:
    string_data = stringio.read()
    return string_data


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
st.text("Upload txt file")
uploaded_file = st.file_uploader("Choose a  txt file")

with  st.form("Form", clear_on_submit=True):
    api_key = st.text_area("Enter your OpenAI key:")

    submitted = st.form_submit_button("Submit")
    if submitted and api_key and uploaded_file:
        with st.spinner('Generating Summary...'):
            os.environ["OPENAI_API_KEY"] = api_key
            text = read_file_as_string(uploaded_file)
            documents = create_documents(text)
            response = generate_summary(documents)

            if len(response):
                st.info(response)
