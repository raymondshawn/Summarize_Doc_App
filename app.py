import langchain
import streamlit as st
from io import StringIO
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os
from langchain.chains.summarize import load_summarize_chain

st.title("🦜️🔗 Summarize  File")
st.text("Upload txt file")
uploaded_file = st.file_uploader("Choose a file")