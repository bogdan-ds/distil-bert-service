import textwrap
from typing import List

from transformers import pipeline, DistilBertTokenizerFast, DistilBertModel

from src.schemas import Entity


def run_nlp_pipeline(tokenizer: DistilBertTokenizerFast,
                     model: DistilBertModel,
                     text: str) -> List[Entity]:
    """
    Run NLP pipeline on text.
    :param tokenizer: loaded tokenizer
    :param model: loaded model
    :param text: input text
    :return: list of entities mapped to the Entity schema
    """
    all_results = []
    chunks = textwrap.wrap(text, 500)
    nlp_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)
    # BERT context is 512 tokens, so we need to split the text into chunks
    offset = 0
    for chunk in chunks:
        ner_results = nlp_pipeline(chunk)
        for result in ner_results:
            result['start'] += offset
            result['end'] += offset
        all_results.extend(ner_results)
        offset += len(chunk) + 1
    mapped_entities = map_ner_results(all_results)
    merged_entities = merge_consecutive_entities(mapped_entities)
    return merged_entities


def merge_consecutive_entities(entities: List[Entity]) -> List[Entity]:
    """
    Merge consecutive entities of the same entity type.
    :param entities: list of entities
    :return: list of merged entities
    """
    if not entities:
        return []

    merged_predictions = []
    current_entity = entities[0].model_copy()

    for i in range(1, len(entities)):
        prev_entity = entities[i - 1]
        current = entities[i]

        if prev_entity.end == current.start:
            current_entity.text += current.text
            current_entity.end = current.end
        else:
            merged_predictions.append(current_entity)
            current_entity = current.model_copy()
    merged_predictions.append(current_entity)

    return merged_predictions


def map_ner_results(ner_results: List[dict]) -> List[Entity]:
    """
    Map NER results to Entity schema.
    :param ner_results: results from NER pipeline
    :return: list of entities mapped to the Entity schema
    """
    mapped_entities = []

    for result in ner_results:
        word = result['word']
        if word.startswith("##"):
            word = word[2:]

        entity = Entity(
            text=word,
            index=result['index'],
            start=result['start'],
            end=result['end'],
            entity_type=result['entity']
        )

        mapped_entities.append(entity)

    return mapped_entities
