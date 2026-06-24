FROM python:3.11-slim

WORKDIR /app
COPY requirements-prod.txt /app/requirements-prod.txt
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY . /app
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production
EXPOSE 8000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "wsgi:app"]
