FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Expose API port
EXPOSE 8000

# Run FastAPI (change if using Flask/Django)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
