# Base image
FROM python:3.14-slim

# Working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy rest of project
COPY . .

# Execute the data processing script
CMD ["python", "src/main.py"]