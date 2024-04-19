import streamlit as st
import tempfile
from scripts import *
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Vectara

from langchain.prompts import PromptTemplate


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
    st.write('## Anomaly detection for document metadata')

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
        st.write(metadata)
