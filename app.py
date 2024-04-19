import streamlit as st
import tempfile
#from scripts import analyze_metadata, generate_metadata, ingest, MODEL_NAME
from scripts import *
import os
import argparse
import sys
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Vectara

from langchain.prompts import PromptTemplate
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# import json
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# from langchain_community.document_loaders import TextLoader
# from langchain_community.document_loaders import UnstructuredPDFLoader

load_dotenv()

#MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

vectara_customer_id = os.environ['VECTARA_CUSTOMER_ID']
vectara_corpus_id = os.environ['VECTARA_CORPUS_ID']
vectara_api_key = os.environ['VECTARA_API_KEY']

embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")

vectara = Vectara(vectara_customer_id=vectara_customer_id,
                  vectara_corpus_id=vectara_corpus_id,
                  vectara_api_key=vectara_api_key)

summary_config = {"is_enabled": True, "max_results": 3, "response_lang": "eng"}
retriever = vectara.as_retriever(
    search_kwargs={"k": 3, "summary_config": summary_config}
)

template = """
passage: You are a helpful assistant that understands BIM building documents.
passage: You will analyze BIM document metadata composed of filename, description, and engineering discipline.
passage: The metadata is written in German.
passage: Filename: {filename}, Description: {description}, Engineering discipline: {discipline}.
query: Does the filename match other filenames within the same discipline?
query: Does the description match the engineering discipline?
query: How different is the metadata to your curated information?
query: Highlight any discrepancies and comment on whether or not the metadata is anomalous.
"""

prompt = PromptTemplate(template=template, input_variables=['filename', 'description', 'discipline'])


def get_sources(documents):
    return documents[:-1]


def get_summary(documents):
    return documents[-1].page_content


if __name__ == "__main__":

    st.title('# DocVerifyRAG')
    st.write('## Anomaly detection for BIM document metadata')

    with st.form('analyze_form'):
        st.write('Enter your file metadata in the following schema:')
        text = st.text_input(label='Filename, Description, Discipline',
                             value="", placeholder=str)
        submitted = st.form_submit_button('Submit')

        if submitted:
            filename, description, discipline = text.split(',')

            st.write('## Analyzing with Vectara + together.ai')
            analysis = analyze_metadata(filename, description, discipline)

            st.write(analysis)

    st.write('## Generate metadata?')
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf", "txt"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.read())
            file_path = tmp.name
            st.write(f'Created temporary file {file_path}')
        FILEPATH = file_path
        docs = ingest(file_path)
        st.write('## Querying Together.ai API')
        metadata = generate_metadata(docs, FILEPATH)
        st.chat_message(metadata)

    """
    parser = argparse.ArgumentParser(description="Generate metadata for a BIM document")
    parser.add_argument("document", metavar="FILEPATH", type=str,
                        help="Path to the BIM document")

    args = parser.parse_args()

    if not os.path.exists(args.document) or not os.path.isfile(args.document):
        print("File '{}' not found or not accessible.".format(args.document))
        sys.exit(-1)

    docs = ingest(args.document)
    metadata = generate_metadata(docs)
    print(metadata)
    """
