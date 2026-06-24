FROM python:3.12-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

ENV FHIR_BASE_URL=http://localhost:8080/fhir

EXPOSE 5001

CMD ["python", "main.py"]