# Currently tested & workong for Python 3.11
FROM python:3.9-slim

# Copy the current directory contents into the container at /app
COPY app /app

# Copy and install the requirements
COPY ./requirements.txt /requirements.txt

# Pip install the dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

# Set the working directory to /app
WORKDIR /app

# Expose port 8501
EXPOSE 8501

# Run the app
CMD streamlit run /app/main.py
