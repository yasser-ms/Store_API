FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#for render
EXPOSE 10000

CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "app:app"]
