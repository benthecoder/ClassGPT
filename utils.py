import streamlit as st
import boto3
from botocore.errorfactory import ClientError

from pprint import pprint
import os
import base64
import logging
import sys
from collections import defaultdict
import openai
import json

from llama_index import GPTSimpleVectorIndex, download_loader
from llama_index.langchain_helpers.chatgpt import ChatGPTLLMPredictor

from dotenv import load_dotenv

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# load OPENAI API KEY
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ------------------- Query GPT ------------------- #


def query_gpt(folder_name, file_name, query):

    if os.getenv("OPENAI_API_KEY") is None:
        st.error("OpenAI API key not set")
        return

    s3 = boto3.resource("s3")
    bucket = s3.Bucket("classgpt")

    index_name = file_name.replace(".pdf", ".json")
    llm_predictor = ChatGPTLLMPredictor()

    if file_exists(folder_name, index_name):

        print("Index found, loading index...")

        index_tmp_path = f"/tmp/{index_name}"
        bucket.download_file(f"{folder_name}/{index_name}", index_tmp_path)
        index = GPTSimpleVectorIndex.load_from_disk(index_tmp_path)

    else:
        print("Index not found, creating new index...")
        pdf_tmp_path = f"/tmp/{file_name}"

        print("Downloading PDF...")
        bucket.download_file(f"{folder_name}/{file_name}", pdf_tmp_path)

        print("Loading PDF as a document...")
        PDFReader = download_loader("PDFReader")
        loader = PDFReader()
        documents = loader.load_data(pdf_tmp_path)

        print("Creating index...")
        index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor)

        print("Saving index...")
        index_tmp_path = f"/tmp/{index_name}.json"
        index.save_to_disk(index_tmp_path)

        print("Uploading index...")
        with open(index_tmp_path, "r") as f:
            json_index = f.read()
            upload_json_to_s3(json_index, f"{folder_name}/{index_name}")

    response = index.query(query, llm_predictor=llm_predictor)

    print(response.get_formatted_sources())

    return response


# ------------------- Render PDF ------------------- #


@st.cache_data()
def show_pdf(folder_name, file_name):

    # open file from s3
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("classgpt")

    file_path = f"/tmp/{file_name}"
    bucket.download_file(f"{folder_name}/{file_name}", file_path)

    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    # create iframe where width is restricted to column size but height is set to 100%
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


# ------------------- S3 Functions ------------------- #


def file_exists(folder_name, file_name):
    s3 = boto3.client("s3")
    bucket_name = "classgpt"

    try:
        s3.head_object(Bucket=bucket_name, Key=f"{folder_name}/{file_name}")
        return True
    except ClientError:
        return False


def folder_exists(bucket, folder_name):
    for _ in bucket.objects.filter(Prefix=f"{folder_name}/"):
        return True
    return False


def create_folder(folder_name):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("classgpt")

    if not folder_exists(bucket, folder_name):
        bucket.put_object(Key=f"{folder_name}/")


def upload_json_to_s3(json_obj, file_path):
    s3 = boto3.client("s3")
    s3.put_object(
        Body=json_obj, Bucket="classgpt", Key=file_path, ContentType="application/json"
    )


def upload_pdf_to_s3(file_obj, file_path):
    s3 = boto3.client("s3")
    s3.upload_fileobj(file_obj, "classgpt", file_path)


def remove_folder(folder_name):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("classgpt")

    if folder_exists(bucket, folder_name):
        for key in bucket.objects.filter(Prefix=f"{folder_name}/"):
            key.delete()
            st.write(f"{key} deleted")


def remove_file(folder_name, file_name):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("classgpt")

    if folder_exists(bucket, folder_name):
        bucket.objects.filter(Prefix=f"{folder_name}/{file_name}").delete(
            Delete={"Objects": [{"Key": f"{folder_name}/{file_name}"}]}
        )


def get_all_files():
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("classgpt")

    classes = defaultdict(list)

    for obj in bucket.objects.all():
        if obj.key.endswith("/"):
            classes[obj.key[:-1]] = []
        else:
            cname, fname = obj.key.split("/")
            if fname.endswith(".pdf"):
                classes[cname].append(fname)

    return classes
