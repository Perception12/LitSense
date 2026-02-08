FROM python:3.12-slim

WORKDIR /app

# Copy requirements from the api folder (build context is project root)
COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 8080

CMD ["python", "-m", "api.app"]
