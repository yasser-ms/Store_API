FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render provides PORT env variable automatically
EXPOSE 5000

CMD ["sh", "-c", "gunicorn wsgi:app -b 0.0.0.0:$PORT"]
