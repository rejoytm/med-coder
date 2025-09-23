import re

from sklearn.metrics.pairwise import cosine_similarity

from data_loader import load_icd10_df, load_icd10_tfidf
from utils import remove_stop_words_and_lemmatize

# Returns a list of ICD-10-CM and ICD-10-PCS codes explicitly mentioned in the text
def extract_icd10_codes(text):
    icd10_pattern = r'''
    \b(
        # ICD-10-CM
        [A-TV-Z][0-9]{2} # Letters A–T or V–Z (excluding U) followed by 2 digits
        (?:\.?[A-Z0-9]{1,4})? # Optionally followed by a dot and 1–4 alphanumeric characters

        |

        # ICD-10-PCS
        [0-9][0-9A-HJ-NP-Z]{6} # A digit followed by 6 alphanumeric characters (excluding letters I and O)
    )\b
    '''
    matches = re.findall(icd10_pattern, text, re.IGNORECASE | re.VERBOSE)
    return [m.upper() for m in matches]

# Returns a list of suggested ICD-10 codes based on similarity between input text and code descriptions
def suggest_icd10_codes(text, max_results_count=10):
    df = load_icd10_df()
    vectorizer, matrix = load_icd10_tfidf()

    preprocessed_text = remove_stop_words_and_lemmatize(text)
    query_vector = vectorizer.transform([preprocessed_text])
    similarity_scores = cosine_similarity(query_vector, matrix).flatten()

    positive_score_indices = [i for i, score in enumerate(similarity_scores) if score > 0]
    top_score_indices = sorted(positive_score_indices, key=lambda i: similarity_scores[i], reverse=True)[:max_results_count]
    top_results = df.iloc[top_score_indices].copy()

    return list(top_results["ICD10_Code"])