# ClassGPT

> ChatGPT for my lecture slides

Built with [LlamaIndex](https://github.com/jerryjliu/gpt_index) and uses the latest [ChatGPT API](https://platform.openai.com/docs/guides/chat) from [OpenAI](https://openai.com/). The lecture pdfs and indices are stored on s3.

The code is pretty spaghetti, but it works.

Inspired by [AthenGPT](http://athensgpt.com/)

## App Demo

https://user-images.githubusercontent.com/49143413/222878151-42354446-5234-41fa-ad36-002dd74a5408.mp4

## How this works

TODO

- explain what llamaindex does
- explain [index](notebooks/index.json) created by LlamaIndex.

## Installation and setup

1. create python env

```bash
    conda create -n classgpt python=3.9
    conda activate classgpt
```

2. create s3 bucket named `"classgpt"`

3. configure aws ([quickstart](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html))

```bash
    aws configure
```

4. rename [.env.local.example] to `.env` and add your openai credentials

5. install dependencies

```bash
    pip install -r requirements.txt
```

6. run streamlit app

```bash
    cd app/
    streamlit run app/01_❓_Ask.py
```

## Docker

```bash
    docker compose up
```

## TODO

- [ ] Host on EC2
- [ ] Compose indices of multiple lectures and query on all of them
  - [ ] selection to choose all lectures
  - [ ] loop through all current index, create the ones that haven't been created, and compose them together
  - [ ] as new slides come in, insert it to the index
  - [ ] query on the composed index
  - references
    - [Composability — LlamaIndex documentation](https://gpt-index.readthedocs.io/en/latest/how_to/composability.html)
    - [gpt_index/ComposableIndices.ipynb](https://github.com/jerryjliu/gpt_index/blob/main/examples/composable_indices/ComposableIndices.ipynb)
- [ ] experiment with custom chatgpt api prompt
- [ ] figure out cloud hosting that accepts openai api key

## FAQ

### Tokens

Tokens can be thought of as pieces of words. Before the API processes the prompts, the input is broken down into tokens. These tokens are not cut up exactly where the words start or end - tokens can include trailing spaces and even sub-words. Here are some helpful rules of thumb for understanding tokens in terms of lengths:

- 1 token ~= 4 chars in English
- 1 token ~= ¾ words
- 100 tokens ~= 75 words
- 1-2 sentence ~= 30 tokens
- 1 paragraph ~= 100 tokens
- 1,500 words ~= 2048 tokens

Try the [OpenAI Tokenizer tool](https://platform.openai.com/tokenizer)

[Source](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)

### Embeddings

An embedding is a vector (list) of floating point numbers. The distance between two vectors measures their relatedness. Small distances suggest high relatedness and large distances suggest low relatedness.

For `text-embedding-ada-002`, cost is $0.0004 / 1k tokens or 3000 pages/dollar

- [Embeddings - OpenAI API](https://platform.openai.com/docs/guides/embeddings/use-cases)
- [What Are Word and Sentence Embeddings?](https://txt.cohere.ai/sentence-word-embeddings/)

## References

### Streamlit

- [How do I increase the upload limit of st.file_uploader on Streamlit Community Cloud? - Streamlit Docs](https://docs.streamlit.io/knowledge-base/deploy/increase-file-uploader-limit-streamlit-cloud)
- [hayabhay/whisper-ui: Streamlit UI for OpenAI's Whisper](https://github.com/hayabhay/whisper-ui)

### LlamaIndex

- [PDF Loader](https://llamahub.ai/l/file-pdf)
- [emptycrown/llama-hub: A library of data loaders for LLMs made by the community -- to be used with GPT Index and/or LangChain](https://github.com/emptycrown/llama-hub/tree/main)
- [LlamaIndex Usage Pattern — LlamaIndex documentation](https://gpt-index.readthedocs.io/en/latest/guides/usage_pattern.html#)
  - [Saving index](https://gpt-index.readthedocs.io/en/latest/guides/usage_pattern.html#optional-save-the-index-for-future-use)
- [gpt_index/SimpleIndexDemo-ChatGPT.ipynb](https://github.com/jerryjliu/gpt_index/blob/main/examples/vector_indices/SimpleIndexDemo-ChatGPT.ipynb)

### Boto3

- [python - boto3 file_upload does it check if file exists - Stack Overflow](https://stackoverflow.com/questions/44978426/boto3-file-upload-does-it-check-if-file-exists)
- [Boto 3: Resource vs Client](https://www.learnaws.org/2021/02/24/boto3-resource-client/)
- [python - Writing json to file in s3 bucket - Stack Overflow](https://stackoverflow.com/questions/46844263/writing-json-to-file-in-s3-bucket)

### Docker stuff

- [amazon web services - What is the best way to pass AWS credentials to a Docker container? - Stack Overflow](https://stackoverflow.com/questions/36354423/what-is-the-best-way-to-pass-aws-credentials-to-a-docker-container)
- [docker-compose up failing due to: error: can't find Rust compiler · Issue #572 · acheong08/ChatGPT](https://github.com/acheong08/ChatGPT/issues/572)
- [software installation - How to install a package with apt without the "Do you want to continue [Y/n]?" prompt? - Ask Ubuntu](https://askubuntu.com/questions/523962/how-to-install-a-package-with-apt-without-the-do-you-want-to-continue-y-n-p)
- [How to use sudo inside a docker container? - Stack Overflow](https://stackoverflow.com/questions/25845538/how-to-use-sudo-inside-a-docker-container)
