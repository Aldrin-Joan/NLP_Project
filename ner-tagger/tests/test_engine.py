import pytest
from ner_engine import extract_nlp_features, extract_entities

def test_extract_nlp_features_basic():
    text = "Apple is looking at buying U.K. startup for $1 billion"
    features = extract_nlp_features(text)
    assert len(features) > 0
    assert features[0]["Text"] == "Apple"
    assert "POS" in features[0]

def test_extract_nlp_features_empty():
    assert extract_nlp_features("") == []
    assert extract_nlp_features("   ") == []

def test_extract_entities_basic():
    text = "Barack Obama was born in Hawaii."
    entities = extract_entities(text)
    assert "Barack Obama" in entities["Person"]
    assert "Hawaii" in entities["Location"]

def test_extract_entities_categories():
    text = "Google was founded on September 4, 1998, in Menlo Park."
    entities = extract_entities(text)
    assert "Google" in entities["Organisation"]
    assert "September 4, 1998" in entities["Date"]
    assert "Menlo Park" in entities["Location"]

def test_extract_entities_empty():
    empty_res = {
        "Person": [],
        "Organisation": [],
        "Location": [],
        "Date": [],
        "Other": []
    }
    assert extract_entities("") == empty_res
