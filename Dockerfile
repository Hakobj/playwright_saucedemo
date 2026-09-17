# Start from Playwright's official image (it has Python + browsers pre-installed)
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (Docker caching trick)
COPY requirements.txt .

# Install Python dependencies
    RUN pip install --no-cache-dir -r requirements.txt

# Create output directory for HTML reports
RUN mkdir -p /app/reports

# Run with exact playwright version
RUN python -m playwright install --with-deps chromium

# Copy the rest of the project
COPY . .

# Default command: run the tests
CMD ["pytest", "--html=reports/report.html", "--self-contained-html"]