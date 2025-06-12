FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gnupg2 \
    curl \
    && echo "deb http://http.kali.org/kali kali-rolling main contrib non-free" > /etc/apt/sources.list.d/kali.list \
    && curl -fsSL https://archive.kali.org/archive-key.asc | apt-key add - \
    && apt-get update && apt-get install -y \
    nmap \
    nikto \
    hydra \
    sqlmap \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@10.2.4

# Set working directory
WORKDIR /app

# Copy backend files
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create backend directory structure
RUN mkdir -p /app/backend/app

# Copy backend files
COPY backend/app/main.py /app/backend/app/
COPY backend/requirements.txt /app/backend/

# Copy frontend files
COPY frontend/ /app/frontend/

# Install frontend dependencies and build
WORKDIR /app/frontend
RUN npm install
RUN npm install react-scripts@5.0.1 --save
RUN npm run build

# Return to app directory
WORKDIR /app

# Copy create_admin.py
COPY app/create_admin.py /app/app/create_admin.py

# Expose ports
EXPOSE 8000 3000

# Start the application
CMD /bin/bash -c "while ! nc -z db 5432; do sleep 1; done; echo 'Database is ready!' && cd /app/backend && PYTHONPATH=/app/backend python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload & cd /app/frontend && npm install && npm start & wait" 