# Container 3: The Test Runner
FROM python:3.11-slim

WORKDIR /tests

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "-v", "-s", "--tb=short", "--html=/tests/reports/report.html", "--self-contained-html"] 
# added -s for possibility of printing something needed for debug purpose  
