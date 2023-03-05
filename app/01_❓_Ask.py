import streamlit as st
from config import get_page_config
from s3 import S3
from utils import query_gpt, show_pdf

st.set_page_config(**get_page_config())

# Session states
# --------------
if "chosen_class" not in st.session_state:
    st.session_state.chosen_class = "--"

if "chosen_pdf" not in st.session_state:
    st.session_state.chosen_pdf = "--"

st.header("ClassGPT: ChatGPT for your lectures slides")

bucket_name = "classgpt"
s3 = S3(bucket_name)

all_classes = s3.list_files()

chosen_class = st.selectbox(
    "Select a class", list(all_classes.keys()) + ["--"], index=len(all_classes)
)

st.session_state.chosen_class = chosen_class

if st.session_state.chosen_class != "--":
    all_pdfs = all_classes[chosen_class]

    chosen_pdf = st.selectbox(
        "Select a PDF file", all_pdfs + ["--"], index=len(all_pdfs)
    )

    st.session_state.chosen_pdf = chosen_pdf

    if st.session_state.chosen_pdf != "--":
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Ask a question")
            st.markdown(
                """
                Here are some prompts:
                - `What is the main idea of this lecture in simple terms?`
                - `Summarize the main points of slide 5`
                - `Provide 5 practice questions on this lecture with answers`
                """
            )
            query = st.text_input("Enter your question")

            if st.button("Ask"):
                with st.spinner("Generating answer..."):
                    res = query_gpt(chosen_class, chosen_pdf, query)
                    st.markdown(res)

        with col2:
            show_pdf(chosen_class, chosen_pdf)
