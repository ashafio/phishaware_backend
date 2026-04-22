FROM python:3.10-slim

RUN apt-get update && apt-get install -y libgomp1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]