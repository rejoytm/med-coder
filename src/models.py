import whisperx
import medspacy

transcription_model = whisperx.load_model("large-v2", device="cpu", compute_type="int8")

nlp_model = medspacy.load(medspacy_enable=["medspacy_sectionizer"], load_rules=False)
