# Currently tested & workong for Python 3.11
FROM python:3.9-slim

# Copy the current directory contents into the container at /app
COPY app /app

# Copy and install the requirements
COPY ./requirements.txt /requirements.txt

# Update default packages
RUN apt-get -qq update

RUN apt-get install -y -q \
    build-essential \
    curl

# install gcc
RUN apt-get -y install gcc

# install rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

ENV PATH="/root/.cargo/bin:${PATH}"


# Pip install the dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

# Set the working directory to /app
WORKDIR /app

# Expose port 8501
EXPOSE 8501

# Run the app
CMD streamlit run /app/01_❓_Ask.py
