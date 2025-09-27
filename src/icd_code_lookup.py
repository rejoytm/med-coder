import re

from sklearn.metrics.pairwise import cosine_similarity

from data_loader import load_icd10_df, load_icd10_tfidf
from utils import remove_stop_words_and_lemmatize

# Extracts ICD-10 codes explicitly mentioned in the input text
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
    unique_matches = list(dict.fromkeys(match.upper() for match in matches))
    return get_valid_icd10_codes_with_descriptions(unique_matches)

# Suggests ICD-10 codes based on similarity between input text and code descriptions
def suggest_icd10_codes(text, max_results_count=10):
    df = load_icd10_df()
    vectorizer, matrix = load_icd10_tfidf()

    preprocessed_text = remove_stop_words_and_lemmatize(text)
    query_vector = vectorizer.transform([preprocessed_text])
    similarity_scores = cosine_similarity(query_vector, matrix).flatten()

    positive_score_indices = [i for i, score in enumerate(similarity_scores) if score > 0]
    top_score_indices = sorted(positive_score_indices, key=lambda i: similarity_scores[i], reverse=True)[:max_results_count]
    top_results = df.iloc[top_score_indices].copy()

    codes = list(top_results["code"])
    return get_valid_icd10_codes_with_descriptions(codes)

# Filters the input list of codes and returns a list of dictionaries with 'code' and 'description' for entries that exist in the ICD-10 dataset
def get_valid_icd10_codes_with_descriptions(codes):
    df = load_icd10_df()

    # Remove periods and uppercase codes for lookup, but retain originals to return at the end
    cleaned_to_original = {
        code.replace(".", "").upper(): code
        for code in codes
    }

    cleaned_codes = list(cleaned_to_original.keys())

    valid_codes = df[df["code"].isin(cleaned_codes)]

    return [
        {
            "code": cleaned_to_original.get(row["code"]),
            "description": row["description"]
        }
        for _, row in valid_codes.iterrows()
    ]