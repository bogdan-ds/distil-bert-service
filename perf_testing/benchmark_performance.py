import requests
import time
import os
import multiprocessing
from concurrent.futures import ThreadPoolExecutor

URL = "http://localhost:8000/ner"


def send_request(data: str) -> float:
    response = requests.post(URL, json={"text": data})
    return response.elapsed.total_seconds()


texts = []
for file in os.listdir():
    if file.endswith(".txt"):
        with open(f"./{file}", "r") as f:
            texts.append(f.read())
single_doc_time = send_request(texts[0])
with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
    start_time = time.time()
    list(executor.map(send_request, texts))
    multiple_docs_time = time.time() - start_time


print(f"Single Document Processing Time: {single_doc_time} seconds")
print(f"Multiple (3) Documents Processing Time: {multiple_docs_time} seconds")
