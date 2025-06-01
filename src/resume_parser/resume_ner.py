import logging
from collections import defaultdict

from transformers import pipeline

from tools.logger import AppLogger

logger = AppLogger(
    name="ResumeNER",
    level=logging.DEBUG,
    log_file=".logs/resume_ner.log",
    console_level=logging.INFO,
    file_level=logging.DEBUG,
)


class ResumeNER:
    def __init__(self, model_name="omarahmed11/resume-ner-model"):
        try:
            self.nlp_ner = pipeline(
                "ner", model=model_name, aggregation_strategy="simple"
            )
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
            logger.info("Starting entity extraction.")
            ner_result = self.nlp_ner(text)
        except Exception as e:
            logger.error(f"Error during entity extraction: {e}")
            return {}

        entities = defaultdict(list)
        for entity in ner_result:
            logger.debug(f"Extracted entity: {entity}")
            entities[entity['entity_group']].append({entity['word']})

        processed_entities = {}
        for key, value_list in entities.items():
            logger.debug(f"Processing entity group: {key} with values: {value_list}")
            processed_entities[key] = list([val for val in value_list])
        return processed_entities




