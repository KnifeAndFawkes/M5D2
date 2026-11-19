FROM python:3.12-slim

# Setting a folder inside the container as the work dir
WORKDIR /app

# Install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the files in the local folder in tho the work dir
COPY . /app

# Run our script at start of container
ENTRYPOINT ["python3","app.py"]