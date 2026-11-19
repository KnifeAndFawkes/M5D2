FROM python:3.12-slim

# Setting a folder inside the container as the work dir
WORKDIR /app

# Copy the files in the local folder in tho the work dir
COPY sqlcreate.py .

# Run our script at start of container
ENTRYPOINT ["python3","sqlcreate.py"]