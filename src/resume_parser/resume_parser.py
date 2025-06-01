import logging
import os
import re

from src.resume_parser.resume_ner import ResumeNER
from src.resume_parser.text_extraction import (
    extract_text_from_image,
    extract_text_from_pdf,
    extract_years_of_experience,
)
from src.tools.logger import AppLogger

logger = AppLogger(
    name="ResumeParser",
    level=logging.DEBUG,
    log_file="parser.log",
    console_level=logging.INFO,
    file_level=logging.DEBUG,
)


class ResumeParser:
    def __init__(self, ner_model_name="omarahmed11/resume-ner-model"):
        self.ner_processor = ResumeNER(model_name=ner_model_name)

    def parse(self, file_path):
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return None

        _, file_extension = os.path.splitext(file_path)
        raw_text = None

        logger.info(f"--- Parsing file: {file_path} ---")

        if file_extension.lower() == ".pdf":
            logger.info("Detected PDF file. Extracting text from PDF.")
            raw_text = extract_text_from_pdf(file_path)
        elif file_extension in [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
            logger.info("Detected image file. Extracting text from image.")
            raw_text = extract_text_from_image(file_path)
        else:
            logger.error(
                f"Unsupported file type: {file_extension}. Only PDF and image files are supported."
            )
            return None

        if not raw_text:
            logger.error("No text extracted from the file.")
            return None

        logger.info("Text extraction successful. Proceeding with NER.")
        entities = self.ner_processor.extract_entities(raw_text)

        years_of_experience = extract_years_of_experience(raw_text)

        if years_of_experience is not None:
            entities["YEARS_OF_EXPERIENCE_ESTIMATED"] = years_of_experience
            logger.info(f"Estimated years of experience: {years_of_experience}")
        else:
            logger.warning("Could not estimate years of experience from the text.")
            entities["YEARS_OF_EXPERIENCE_ESTIMATED"] = None

        contact_info = entities.get("CONTACT_INFO", [])
        emails = []
        phones = []
        linkedin_profiles = []

        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        phone_pattern = r"\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
        linkedin_pattern = r"(linkedin\.com/in/[\w-]+)"

        for info in contact_info:
            found_emails = re.findall(email_pattern, info)
            if found_emails:
                emails.extend(found_emails)

            found_phones = re.findall(phone_pattern, info)
            if found_phones:
                phones.extend(found_phones)

            found_linkedin = re.findall(linkedin_pattern, info, re.IGNORECASE)
            if found_linkedin:
                linkedin_profiles.extend(found_linkedin)

        if emails:
            entities["EMAILS"] = list(set(emails))
        if phones:
            entities["PHONES"] = list(set(phones))
        if linkedin_profiles:
            entities["LINKEDIN_PROFILES"] = list(set(linkedin_profiles))

        if "CONTACT_INFO" in entities and (emails or phones or linkedin_profiles):
            pass  # Keep it for now, it might contain other things like address

        return {
            "file_path": file_path,
            "raw_text_snippet": raw_text[:200] + "..." if raw_text else "",
            "entities": entities,
        }