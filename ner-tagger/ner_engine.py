import spacy
import pandas as pd
from typing import List, Dict, Any, Optional

# Load the spaCy model once at module level
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback to help user identify missing model
    nlp = None

ENTITY_CATEGORY_MAP = {
    "PERSON": "Person",
    "ORG": "Organisation",
    "GPE": "Location",
    "LOC": "Location",
    "DATE": "Date"
}

def extract_nlp_features(text: str) -> List[Dict[str, Any]]:
    """
    Extracts token-level features from the provided text.
    
    Args:
        text: The input string to process.
        
    Returns:
        A list of dictionaries containing token text, lemma, POS, tag, and dependency.
        Returns an empty list if nlp model is not loaded or text is empty.
    """
    if not nlp or not text.strip():
        return []

    doc = nlp(text)
    data = []
    
    for token in doc:
        data.append({
            "Text": token.text,
            "Morpheme/Stem": token.lemma_,
            "POS": token.pos_,       
            "Tag": token.tag_,        
            "Dependency": token.dep_
        })
    
    return data

def extract_entities(text: str) -> Dict[str, List[str]]:
    """
    Extracts named entities from the text and groups them into categories.
    
    Categories: Person, Organisation, Location, Date, Other.
    GPE and LOC are both mapped to Location.
    
    Args:
        text: The input string to process.
        
    Returns:
        A dictionary mapping category names to lists of entity strings.
    """
    grouped = {
        "Person": [],
        "Organisation": [],
        "Location": [],
        "Date": [],
        "Other": []
    }

    if not nlp or not text.strip():
        return grouped

    doc = nlp(text)
    
    for ent in doc.ents:
        category = ENTITY_CATEGORY_MAP.get(ent.label_, "Other")
        
        # Format for 'Other' to include original label
        entity_text = ent.text
        if category == "Other":
            entity_text = f"{ent.text} ({ent.label_})"
            
        if entity_text not in grouped[category]:
            grouped[category].append(entity_text)
            
    return grouped
