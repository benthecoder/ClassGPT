import streamlit as st
from streamlit_option_menu import option_menu

from utils import (
    create_folder,
    get_all_files,
    query_gpt,
    remove_file,
    remove_folder,
    show_pdf,
    upload_pdf_to_s3,
)


def main():
    st.set_page_config(
        page_title="ClassGPT",
        page_icon=":books:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    if "chosen_class" not in st.session_state:
        st.session_state.chosen_class = "--"

    if "chosen_pdf" not in st.session_state:
        st.session_state.chosen_pdf = "--"

    with st.sidebar:
        choose = option_menu(
            "ClassGPT",
            [
                "Ask",
                "Data",
            ],
            # https://icons.getbootstrap.com/
            icons=["question", "files"],
            menu_icon="book",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "000"},
                "icon": {"color": "white", "font-size": "20px"},
                "nav-link": {
                    "font-size": "20px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#000",
                },
                "nav-link-selected": {"background-color": "blue"},
            },
        )

    if choose == "Ask":

        st.header("ClassGPT: ChatGPT for your lectures slides")

        all_classes = get_all_files()

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
                    query = st.text_input("Enter your question")

                    if st.button("Ask"):

                        with st.spinner("Generating answer..."):
                            res = query_gpt(chosen_class, chosen_pdf, query)
                            st.write(res)

                with col2:
                    show_pdf(chosen_class, chosen_pdf)

    elif choose == "Data":

        all_classes = get_all_files()

        tab1, tab2, tab3 = st.tabs(["Upload data", "Add Class", "Delete"])

        with tab1:

            st.subheader("Upload new lectures")

            chosen_class = st.selectbox(
                "Select a class",
                list(all_classes.keys()) + ["--"],
                index=len(all_classes),
            )

            st.write("Don't see your class? Add it in the next tab.")

            if chosen_class != "--":

                with st.form("upload_pdf"):
                    uploaded_files = st.file_uploader(
                        "Upload a PDF file", type="pdf", accept_multiple_files=True
                    )

                    submit_button = st.form_submit_button("Upload")

                    if submit_button:

                        with st.spinner("Uploading files..."):
                            for uploaded_file in uploaded_files:
                                upload_pdf_to_s3(
                                    uploaded_file,
                                    f"{chosen_class}/{uploaded_file.name}",
                                )

                            st.success(f"{len(uploaded_files)} files uploaded")

        with tab2:

            st.subheader("Add a new class")

            with st.form("add_class"):
                add_class = st.text_input("Enter a new class name")

                submit_button = st.form_submit_button("Add")

                if submit_button:
                    create_folder(add_class)
                    st.success(f"Class {add_class} added")

        with tab3:

            st.subheader("Delete a class or a PDF file")

            chosen_class = st.selectbox(
                "Select a class to delete",
                list(all_classes.keys()) + ["--"],
                index=len(all_classes),
            )

            if chosen_class != "--":

                all_pdfs = all_classes[chosen_class] + ["all"]

                chosen_pdf = st.selectbox(
                    "Select a PDF file",
                    all_pdfs + ["--"],
                    index=len(all_pdfs),
                )

                if chosen_pdf != "--":
                    submit_button = st.button("Remove")

                    if submit_button:

                        if chosen_pdf == "all":
                            remove_folder(chosen_class)
                            st.success(f"{chosen_class} removed")
                        else:
                            remove_file(chosen_class, chosen_pdf)
                            st.success(f"{chosen_pdf} removed")


if __name__ == "__main__":
    main()
