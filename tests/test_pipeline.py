from src.schemas import Entity
from src.pipeline import map_ner_results, merge_consecutive_entities

from tests.mocks import mocked_ner_results, consecutive_entities


def test_map_ner_results():
    mapped_entities = map_ner_results(mocked_ner_results)
    assert len(mapped_entities) == 7
    assert mapped_entities[0] == Entity(
        text='Framework', entity_type='B-MISC', index=7, start=36, end=45)
    assert mapped_entities[1] == Entity(
        text='13', entity_type='I-MISC', index=8, start=46, end=48)
    assert mapped_entities[2] == Entity(
        text='EC', entity_type='B-ORG', index=20, start=82, end=84)
    assert mapped_entities[3] == Entity(
        text='Google', entity_type='B-MISC', index=35, start=150, end=156)
    assert mapped_entities[4] == Entity(
        text='Ch', entity_type='I-MISC', index=36, start=157, end=159)
    assert mapped_entities[5] == Entity(
        text='rome', entity_type='I-MISC', index=37, start=159, end=163)
    assert mapped_entities[6] == Entity(
        text='book', entity_type='I-MISC', index=38, start=163, end=167)


def test_merge_consecutive_entities():
    merged_entities = merge_consecutive_entities(consecutive_entities)
    assert merged_entities[0] == Entity(
        text='Chromebook', entity_type='B-MISC', index=36, start=157, end=167)
