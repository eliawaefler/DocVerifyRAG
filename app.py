import io
import os
import streamlit as st
import tempfile

from scripts import generate_metadata, ingest, MODEL_NAME


st.title('DocVerifyRAG')
st.write('Anomaly detection for BIM document metadata')

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf","txt"])

if uploaded_file is not None:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.read())
            file_path = tmp.name
            st.write(f'Created temporary file {file_path}')

        docs = ingest(file_path)
        st.write('## Querying Together.ai API')
        metadata = generate_metadata(docs)
        st.write(f'## Metadata Generated by {MODEL_NAME}')
        st.write(metadata)

        # Clean up the temporary file
        os.remove(file_path)

    except Exception as e:
        st.error(f'Error: {e}')