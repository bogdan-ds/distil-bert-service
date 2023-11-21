FROM python:3.8

WORKDIR /app

COPY src/ /app/src
COPY requirements.txt /app
EXPOSE 8000
RUN pip install --no-cache -r requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0" , "--port", "8000"]
