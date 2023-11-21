import psutil
import time
import transformers

from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.pipeline import run_nlp_pipeline
from src.schemas import NERRequest, NERResponse
from src.utils import get_system_metrics


distil_bert = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Load model and tokenizer on startup and clear them on shutdown. Measure the
    model and tokenizer loading time and add to context.
    """
    # Most downloaded fine-tuned distilBERT model on HF, fine-tuned for NER.
    # Prepared by Elastic
    start_time = time.time()
    distil_bert['tokenizer'] = transformers.DistilBertTokenizerFast.\
        from_pretrained("elastic/"
                        "distilbert-base-cased-finetuned-conll03-english")
    distil_bert['model'] = transformers.DistilBertForTokenClassification.\
        from_pretrained("elastic/"
                        "distilbert-base-cased-finetuned-conll03-english")
    startup_time = time.time() - start_time
    distil_bert['startup_time'] = startup_time
    yield
    distil_bert.clear()


app = FastAPI(lifespan=lifespan)


@app.post("/ner", response_model=NERResponse)
def process_ner(request: NERRequest) -> NERResponse:
    """
    REST endpoint for NER processing.
    :param: NERRequest schema
    :return: NERResponse schema
    """
    process = psutil.Process()
    mem_usage_before = process.memory_info().rss
    start_time = time.time()
    entities = run_nlp_pipeline(distil_bert['tokenizer'],
                                distil_bert['model'],
                                request.text)
    elapsed_time = time.time() - start_time
    mem_usage_after = process.memory_info().rss
    mem_used = mem_usage_after - mem_usage_before
    return NERResponse(text=request.text, entities=entities,
                       elapsed_time=elapsed_time, estimated_memory=mem_used)


@app.get("/metrics")
def get_metrics() -> dict:
    """
    REST endpoint for getting system metrics.
    :return: dict
    """
    usage = get_system_metrics()
    usage['startup_time'] = distil_bert['startup_time']
    return usage
