import base64
import logging
import os
import sys

import openai
import streamlit as st
from dotenv import load_dotenv
from llama_index import GPTSimpleVectorIndex, download_loader
from llama_index.langchain_helpers.chatgpt import ChatGPTLLMPredictor
from s3 import S3

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# load OPENAI API KEY
load_dotenv()
if os.getenv("OPENAI_API_KEY") is None:
    st.error("OpenAI API key not set")
openai.api_key = os.getenv("OPENAI_API_KEY")

s3 = S3("classgpt")

# ------------------- Query GPT ------------------- #


@st.cache_resource(show_spinner=False)
def get_index(folder_name, file_name):
    """
    Get the index for a given PDF file. If the index does not exist, create it.
    """

    index_name = file_name.replace(".pdf", ".json")
    llm_predictor = ChatGPTLLMPredictor()

    if s3.file_exists(folder_name, index_name):
        logging.info("Index found, loading index...")
        index_tmp_path = f"/tmp/{index_name}"
        s3.download_file(f"{folder_name}/{index_name}", index_tmp_path)
        index = GPTSimpleVectorIndex.load_from_disk(index_tmp_path)
    else:
        logging.info("Index not found, creating new index...")
        pdf_tmp_path = f"/tmp/{file_name}"

        logging.info("Downloading PDF...")
        s3.download_file(f"{folder_name}/{file_name}", pdf_tmp_path)

        logging.info("Loading PDF as a document...")
        PDFReader = download_loader("PDFReader")
        loader = PDFReader()
        documents = loader.load_data(pdf_tmp_path)

        logging.info("Creating index...")
        index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor)

        logging.info("Saving index...")
        index_tmp_path = f"/tmp/{index_name}.json"
        index.save_to_disk(index_tmp_path)

        logging.info("Uploading index to s3...")
        with open(index_tmp_path, "rb") as f:
            s3.upload_files(f, f"{folder_name}/{index_name}")

    return index


def query_gpt(chosen_class, chosen_pdf, query):
    llm_predictor = ChatGPTLLMPredictor()
    index = get_index(chosen_class, chosen_pdf)
    response = index.query(query, llm_predictor=llm_predictor)

    # logging.info(response.get_formatted_sources())

    return response


# ------------------- Render PDF ------------------- #


@st.cache_data()
def show_pdf(folder_name, file_name):
    file_path = f"/tmp/{file_name}"
    s3.download_file(f"{folder_name}/{file_name}", file_path)

    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    pdf_display = f"""
    <iframe
        src="data:application/pdf;base64,{base64_pdf}"
        width="100%" height="1000"
        type="application/pdf"
        style="min-width: 400px;"
    >
    </iframe>
    """

    st.markdown(pdf_display, unsafe_allow_html=True)
