import spacy
import logging
from typing import List
from langdetect import detect, DetectorFactory
from schemas import TokenFeature, EntityResult

# Ensure consistent language detection results
DetectorFactory.seed = 0

logger = logging.getLogger(__name__)


class NLPEngine:
    """
    Singleton NLP Engine for managing Spacy models and extraction logic.
    """
    _instance = None
    _models = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NLPEngine, cls).__new__(cls)
        return cls._instance

    @property
    def is_model_loaded(self) -> bool:
        """Checks if at least one model is loaded."""
        return "en" in self._models

    def load_model(self, lang: str = "en"):
        """
        Loads the appropriate model for the given language.
        """
        if lang in self._models:
            return self._models[lang]

        try:
            # We only have English small model installed in this environment.
            if lang == "en":
                model_name = "en_core_web_sm"
            else:
                # Fallback to English for unknown languages
                model_name = "en_core_web_sm"

            logger.info("Loading Spacy model: %s", model_name)
            self._models[lang] = spacy.load(model_name)
            return self._models[lang]
        except OSError:
            logger.error("Failed to load Spacy model for lang: %s", lang)
            return None

    def detect_language(self, text: str) -> str:
        """
        Identifies the primary language of the text.
        """
        try:
            return detect(text)
        except Exception:
            return "en"

    def extract_nlp_features(self, text: str,
                             model_lang: str = "en") -> List[TokenFeature]:
        """
        Extracts token-level features.
        """
        nlp = self.load_model(model_lang)
        if not nlp or not text.strip():
            return []

        doc = nlp(text)
        features = []

        for token in doc:
            features.append(TokenFeature(
                text=token.text,
                lemma=token.lemma_,
                pos=token.pos_,
                tag=token.tag_,
                dependency=token.dep_
            ))

        return features

    def extract_entities(self, text: str,
                         model_lang: str = "en") -> EntityResult:
        """
        Extracts named entities and groups them.
        """
        nlp = self.load_model(model_lang)
        result = EntityResult()

        if not nlp or not text.strip():
            return result

        doc = nlp(text)

        entity_map = {
            "PERSON": "person",
            "ORG": "organisation",
            "GPE": "location",
            "LOC": "location",
            "DATE": "date"
        }

        for ent in doc.ents:
            category = entity_map.get(ent.label_, "other")
            entity_text = ent.text

            if category == "other":
                entity_text = f"{ent.text} ({ent.label_})"

            target_list = getattr(result, category)
            if entity_text not in target_list:
                target_list.append(entity_text)

        return result


# Export singleton instance
engine = NLPEngine()
