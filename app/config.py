ABOUT = """
### ClassGPT

ClassGPT is a chatbot that answers questions about your lecture slides.

Please report any bugs or issues on [Github](https://github.com/benthecoder/ClassGPT/issues). Thanks!
"""


def get_page_config(layout="wide"):
    return {
        "page_title": "ClassGPT",
        "page_icon": "🤖",
        "layout": layout,
        "initial_sidebar_state": "expanded",
        "menu_items": {
            "Get Help": "https://twitter.com/benthecoder1",
            "Report a bug": "https://github.com/benthecoder/ClassGPT/issues",
            "About": ABOUT,
        },
    }
