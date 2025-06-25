FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SOURCE_ADDRESS=localhost \
    SOURCE_PORT=30015 \
    SOURCE_USER=admin \
    SOURCE_PASSWORD=admin_pass \
    TARGET_ADDRESS=localhost \
    TARGET_PORT=30015 \
    TARGET_USER=admin \
    TARGET_PASS_WORD=admin_pass \
    SOURCE_TABLE=MY_SCHEMA.SOURCE_TABLE \
    TARGET_TABLE=MY_SCHEMA.TARGET_TABLE \
    BATCH_SIZE=1000 \
    ORDER_BY=ID \
    FILENAME=logfile.txt

CMD ["python", "main.py"]
