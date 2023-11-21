from typing import List
from pydantic import BaseModel, Field


class NERRequest(BaseModel):
    """NER Input model.

    Attributes:
        text: Text to be processed
    """
    text: str = Field(..., example="Sample text for NER processing",
                      min_length=8)


class Entity(BaseModel):
    """Named Entity model.

    Attributes:
        text: Entity text
        entity_type: Entity name
        index: Index of entity in text
        start: Start index of entity in text
        end: End index of entity in text
    """
    text: str
    entity_type: str
    index: int
    start: int
    end: int


class NERResponse(BaseModel):
    """NER Output model.

    Attributes:
        text: Original text
        entities: List of entities found in text
    """
    text: str
    entities: List[Entity]
    elapsed_time: float
    estimated_memory: int
