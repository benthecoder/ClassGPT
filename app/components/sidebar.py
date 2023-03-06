import streamlit as st


def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Go 📁 Data page\n"
            "2. Add a class\n"
            "3. Upload lectures for that class\n"
            "3. Ask a question on the ❓ Ask page\n"
        )
        # api_key_input = st.text_input(
        #    "OpenAI API Key",
        #    type="password",
        #    placeholder="sk-xxx...",
        #    help="Get an API key here 👉 https://platform.openai.com/account/api-keys.",
        #    value=st.session_state.get("OPENAI_API_KEY", ""),
        # )

        # if api_key_input:
        #    st.session_state["OPENAI_API_KEY"] = api_key_input

        st.markdown(
            """
            ---
            ## About

            ClassGPT lets you ask questions about your class \
                lectures and get accurate answers

            This tool is a work in progress.

            Contributions are welcomed on [GitHub](https://github.com/benthecoder/ClassGPT)

            Made with ♥️ by [Benedict Neo](https://benneo.super.site/)
            """
        )
