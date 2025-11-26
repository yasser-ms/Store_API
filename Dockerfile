FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Use the PORT variable from Render
CMD ["sh", "-c", "flask run --port=$PORT --host=0.0.0.0"]
