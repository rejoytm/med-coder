from transcription import transcribe
from soap_sectionizer import sectionize_soap_note
from icd_code_lookup import extract_icd10_codes, suggest_icd10_codes

# Transcribes audio SOAP notes and returns a dictionary with 'soap_sections', 'extracted_icd10_codes', and 'suggested_icd10_codes'
def transcribe_and_code_soap_note(audio_path):
    text = transcribe(audio_path)
    sections = sectionize_soap_note(text)
    extracted_icd10_codes = extract_icd10_codes(text)

    """
    When suggesting ICD-10 codes, we focus on section categories 
    that are most likely to contain relevant clinical descriptions.
    """

    categories_for_icd_code_suggestion = [
        "history_of_present_illness",
        "assessment_and_plan"
    ]

    # Create a lookup dictionary from section category to its text
    category_to_text = {s["category"]: s["text"] for s in sections}

    # Concatenate text from selected categories (if present)
    text_for_icd_code_suggestion = " ".join(
        category_to_text[category] 
        for category in categories_for_icd_code_suggestion 
        if category in category_to_text
    ).strip()

    suggested_icd10_codes = suggest_icd10_codes(text_for_icd_code_suggestion)

    return {
        "soap_sections": sections,
        "extracted_icd10_codes": extracted_icd10_codes,
        "suggested_icd10_codes": suggested_icd10_codes
    }