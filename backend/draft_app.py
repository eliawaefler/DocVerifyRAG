import time
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import os
import pickle
from datetime import datetime
from backend.generate_metadata import generate_metadata, ingest


css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''
bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" 
        style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''
user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/rdZC7LZ/Photo-logo-1.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        # Display user message
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            print(message)
            # Display AI response
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

            # THIS DOESNT WORK, SOMEONE PLS FIX
            # Display source document information if available in the message
            if hasattr(message, 'source') and message.source:
                st.write(f"Source Document: {message.source}", unsafe_allow_html=True)


def safe_vec_store():
    # USE VECTARA INSTEAD
    os.makedirs('vectorstore', exist_ok=True)
    filename = 'vectores' + datetime.now().strftime('%Y%m%d%H%M') + '.pkl'
    file_path = os.path.join('vectorstore', filename)
    vector_store = st.session_state.vectorstore

    # Serialize and save the entire FAISS object using pickle
    with open(file_path, 'wb') as f:
        pickle.dump(vector_store, f)


def main():
    st.set_page_config(page_title="Doc Verify RAG", page_icon=":hospital:")
    st.write(css, unsafe_allow_html=True)
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = False
    if "openai_org" not in st.session_state:
        st.session_state.openai_org = False
    if "classify" not in st.session_state:
        st.session_state.classify = False
    def set_pw():
        st.session_state.openai_api_key = True
    st.subheader("Your documents")
    # OPENAI_ORG_ID = st.text_input("OPENAI ORG ID:")
    OPENAI_API_KEY = st.text_input("OPENAI API KEY:", type="password",
                                   disabled=st.session_state.openai_api_key, on_change=set_pw)
    if st.session_state.classify:
        pdf_doc = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=False)
    else:
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        filenames = [file.name for file in pdf_docs if file is not None]
    if st.button("Process"):
        with st.spinner("Processing"):
            if st.session_state.classify:
                # THE CLASSIFICATION APP
                st.write("Classifying")
                plain_text_doc = ingest(pdf_doc.name)
                classification_result = generate_metadata(plain_text_doc)
                st.write(classification_result)
            else:
                # NORMAL RAG
                loaded_vec_store = None
                for filename in filenames:
                    if ".pkl" in filename:
                        file_path = os.path.join('vectorstore', filename)
                        with open(file_path, 'rb') as f:
                            loaded_vec_store = pickle.load(f)
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vec = get_vectorstore(text_chunks)
                if loaded_vec_store:
                    vec.merge_from(loaded_vec_store)
                    st.warning("loaded vectorstore")
                if "vectorstore" in st.session_state:
                    vec.merge_from(st.session_state.vectorstore)
                    st.warning("merged to existing")
                st.session_state.vectorstore = vec
                st.session_state.conversation = get_conversation_chain(vec)
        st.success("data loaded")


    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Doc Verify RAG :hospital:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)
    with st.sidebar:

        st.subheader("Classification Instrucitons")
        classifier_docs = st.file_uploader("Upload your instructions here and click on 'Process'", accept_multiple_files=True)
        filenames = [file.name for file in classifier_docs if file is not None]

        if st.button("Process Classification"):
            st.session_state.classify = True
            with st.spinner("Processing"):
                st.warning("set classify")
                time.sleep(3)


        # Save and Load Embeddings
        if st.button("Save Embeddings"):
            if "vectorstore" in st.session_state:
                safe_vec_store()
                # st.session_state.vectorstore.save_local("faiss_index")
                st.sidebar.success("saved")
            else:
                st.sidebar.warning("No embeddings to save. Please process documents first.")

        if st.button("Load Embeddings"):
            st.warning("this function is not in use, just upload the vectorstore")


if __name__ == '__main__':
    main()
