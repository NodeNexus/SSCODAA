# Use the official Microsoft Playwright image which includes all required OS dependencies
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# Run everything as root (default for this container) to avoid permission issues
WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . /app

# Ensure we are in the correct directory for the server
WORKDIR /app/backend

# Render dynamically assigns a port to the PORT environment variable
# The server.py has been updated to read os.environ.get("PORT", 5000)
CMD ["python", "server.py"]
