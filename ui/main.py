import os
import requests

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

EXTERNAL_NER_API_URL = os.getenv("EXTERNAL_NER_API_URL",
                                 "http://localhost:8000/ner")


@app.get("/")
async def get_ner_form(request: Request):
    return templates.TemplateResponse("ner_form.html", {"request": request})


@app.post("/process-ner")
async def process_ner(request: Request, text: str = Form(...)):
    response = requests.post(EXTERNAL_NER_API_URL, json={"text": text})

    if response.status_code == 200:
        original_text = response.json()["text"]
        entities = response.json()["entities"]
        elapsed_time = round(response.json()["elapsed_time"], 3)
        memory_used = (response.json()["estimated_memory"] / (1024 * 1024))

        return templates.TemplateResponse("ner_display.html",
                                          {"request": request,
                                           "original_text": original_text,
                                           "entities": entities,
                                           "elapsed_time": elapsed_time,
                                           "memory_used": memory_used})
    else:
        error_message = response.text
        return templates.TemplateResponse("error.html",
                                          {"request": request,
                                           "error_message": error_message})
