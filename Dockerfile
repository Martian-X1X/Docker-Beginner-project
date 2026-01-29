FROM python:3.11

WORKDIR /app

# Install Redis client and Flask
RUN pip install redis flask

# Copy app
COPY app.py .

# Run Python unbuffered
CMD ["python", "-u", "app.py"]
