
import os

import streamlit as st

def sidebar():
    with st.sidebar:
        st.markdown("## How to use")
        st.markdown("- Select a class and PDF file")
        st.markdown("- Ask a question in the textbox")
        
        api_key = st.text_input(
            "OpenAI API Key", 
            type="password",
            help="Get your API key at https://platform.openai.com/account/api-keys"
        )
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
            st.success("API key set")
            
        st.markdown("Made with ❤️ by [Benedict Neo](https://benneo.super.site/)")
