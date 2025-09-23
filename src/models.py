import whisperx
import spacy
import medspacy

transcription_model = whisperx.load_model("large-v2", device="cpu", compute_type="int8")

nlp_model = spacy.load("en_core_web_sm", disable=["ner", "parser"])
nlp_model = medspacy.load(nlp_model, medspacy_enable=["medspacy_sectionizer"], load_rules=False)