FROM python:3.8

WORKDIR /app

COPY . /app
EXPOSE 8000
RUN pip install -r requirements.txt

ENV EXTERNAL_NER_API_URL="http://api:8000/ner"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0" , "--port", "8001"]
