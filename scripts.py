import os
import argparse
import json
import openai
import sys

import streamlit
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Vectara
from langchain.prompts import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re


def json_from_string(input_string):
    # Use a regular expression to find text that starts with '{' and ends with '}'
    match = re.search(r'\{[^{}]*\}', input_string)
    if match:
        # Extract the potential JSON string
        potential_json = match.group(0)
        try:
            # Attempt to parse the extracted string as JSON
            parsed_json = json.loads(potential_json)
            # Return the parsed JSON if successful
            return json.dumps(parsed_json)
        except json.JSONDecodeError:
            # Handle cases where the JSON is not valid
            # Attempt to fix common issues like missing quotes
            corrected_json = re.sub(r'(\b\w+\b):', r'"\1":', potential_json)
            corrected_json = re.sub(r': (\b\w+\b)([,\}])', r': "\1"\2', corrected_json)
            try:
                # Try parsing again with the corrected string
                parsed_json = json.loads(corrected_json)
                return json.dumps(parsed_json)
            except json.JSONDecodeError:
                # Return a default JSON object if it still fails
                return json.dumps({"error": "No valid JSON found"})
    else:
        # Return a default JSON object if no potential JSON string is found
        return json.dumps({"error": "No JSON-like data detected"})

# load_dotenv()

MODEL_NAME = "mistralai/Mixtral-8x7B-Instruct-v0.1"

embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")


try:
    vectara_customer_id = os.environ['VECTARA_CUSTOMER_ID']
    vectara_corpus_id = os.environ['VECTARA_CORPUS_ID']
    vectara_api_key = os.environ['VECTARA_API_KEY']
except:
    vectara_customer_id = streamlit.secrets['VECTARA_CUSTOMER_ID']
    vectara_corpus_id = streamlit.secrets['VECTARA_CORPUS_ID']
    vectara_api_key = streamlit.secrets['VECTARA_API_KEY']


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
query: Highligh any discrepancies and comment on wether or not the metadata is anomalous.
"""

prompt = PromptTemplate(template=template, input_variables=['filename', 'description', 'discipline'])


def get_sources(documents):
    return documents[:-1]

def get_summary(documents):
    return documents[-1].page_content

def ingest(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == '.pdf':
        loader = UnstructuredPDFLoader(file_path)
    elif extension == '.txt':
        loader = TextLoader(file_path)
    else:
        raise NotImplementedError('Only .txt or .pdf files are supported')

    # transform locally
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0,
    separators=[
        "\n\n",
        "\n",
        " ",
        ",",
        "\uff0c",  # Fullwidth comma
        "\u3001",  # Ideographic comma
        "\uff0e",  # Fullwidth full stop
        # "\u200B",  # Zero-width space (Asian languages)
        # "\u3002",  # Ideographic full stop (Asian languages)
        "",
    ])
    docs = text_splitter.split_documents(documents)

    return docs


def generate_metadata(docs, my_file_path):
    prompt_template = """
    BimDiscipline = ['plumbing', 'network', 'heating', 'electrical', 'ventilation', 'architecture']

    You are a helpful assistant that understands BIM documents and engineering disciplines. Your answer should be in JSON format and only include the filename, a short description, and the engineering discipline the document belongs to, distinguishing between {[d.value for d in BimDiscipline]} based on the given document."

    Analyze the provided document, which could be in either German or English. Extract the filename, its description, and infer the engineering discipline it belongs to. Document:
    context="
    """     
    # plain text     
    filepath = [doc.metadata for doc in docs][0]['source']
    context = "".join(
        [doc.page_content.replace('\n\n','').replace('..','') for doc in docs])

    prompt = f'{prompt_template}{context}"\nFilepath:{filepath}'

    #print(prompt)
    try:
        together_api_key = os.environ["TOGETHER_API_KEY"]
    except:
        together_api_key = streamlit.secrets["TOGETHER_API_KEY"]
    # Create client
    client = openai.OpenAI(
        base_url="https://api.together.xyz/v1",
        api_key=together_api_key,
        #api_key=userdata.get('TOGETHER_API_KEY'),    
    )

    # Call the LLM with the JSON schema
    chat_completion = client.chat.completions.create(
        model=MODEL_NAME,        
        messages=[
            {
                "role": "system",
                "content": f"You are a helpful assistant that responsds in JSON format"                
            },
            {
                "role": "user",
                "content": prompt                                
            }
        ]
    )
    stringanswer = str(chat_completion.choices[0].message.content)
    print(stringanswer)
    return json.loads(json_from_string(stringanswer))


def analyze_metadata(filename, description, discipline):
    formatted_prompt = prompt.format(filename=filename, description=description, discipline=discipline)
    return (retriever | get_summary).invoke(formatted_prompt)


if __name__ == "__main__":


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