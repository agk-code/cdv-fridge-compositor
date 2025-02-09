FROM python:3.8-slim

RUN apt-get update && apt-get install -y \
    gcc \
    pip \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
COPY swagger.yaml .
COPY app.py .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py", "--host", "0.0.0.0", "--debug"]