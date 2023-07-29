
import openai
import streamlit as st

from dotenv import load_dotenv
load_dotenv()
  
if st.secrets["OPENAI_API_KEY"] is None:
  st.error("OpenAI API key not set")
else:
  openai.api_key = st.secrets["OPENAI_API_KEY"]

def query_gpt(chosen_class, chosen_pdf, query):
  response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f"Answer the question about {chosen_class} and {chosen_pdf}: {query}",
    max_tokens=500,
    n=1,
    stop=None,
    temperature=0.5,
  )
  
  return response.choices[0].text
