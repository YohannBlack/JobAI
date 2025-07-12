import tempfile
from flask import Flask, request, jsonify
import uuid, os, tempfile, logging
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
# Charger le modèle Camembert NER
model_name = "Jean-Baptiste/camembert-ner"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForTokenClassification.from_pretrained(model_name)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")