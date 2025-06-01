import logging
from collections import defaultdict

from transformers import pipeline

from src.tools.logger import AppLogger

logger = AppLogger(
    name="ResumeParser",
    level=logging.DEBUG,
    log_file="parser.log",
    console_level=logging.INFO, 
    file_level=logging.DEBUG,
)


class ResumeNER:
    def __init__(self, model_name="omarahmed11/resume-ner-model"):
        try:
            self.nlp_ner = pipeline("ner", model_name=model_name, aggregation_strategy="simple")
            logger.info(f"Loaded NER model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load NER model {model_name}: {e}")
            self.nlp_ner = None

    def extract_entities(self, text):
        if not self.nlp_ner:
            logger.error("NER model is not loaded. Cannot extract entities.")
            return {}
        if not text or not text.strip():
            logger.error("Input text is empty or None. Cannot extract entities.")
            return {}

        try:
            ner_result = self.nlp_ner(text)
        except Exception as e:
            logger.error(f"Error during entity extraction: {e}")
            return {}

        entities = defaultdict(list)
        for entity in ner_result:
            entities[entity['entity_group']].append({entity['word']})

        processed_entities = {}
        for key, value_list in entities.items():
            processed_entities[key] = list(
                set([val.strip() for val in value_list if val.strip()])
            )
        return processed_entities




