import os
import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from utils import remove_stop_words_and_lemmatize

# Paths to raw files
ICD10CM_RAW_PATH = "data/icd10cm_order_2026.txt"
ICD10PCS_RAW_PATH = "data/icd10pcs_order_2026.txt"

# Paths to generated files
ICD10_DF_PATH = "data/icd10_df.pickle"
ICD10_TFIDF_PATH = 'data/icd10_tfidf.pickle'

def parse_icd10_raw_file(filepath):
    # Define column widths based on the file spec
    colspecs = [
        (6, 13),   # ICD code starts at position 7 and goes till position 13
        (77, None) # Long description starts at position 78 and goes till the end
    ]
    names = ["code", "description"]

    df = pd.read_fwf(filepath, colspecs=colspecs, names=names)
    df["code"] = df["code"].str.strip()
    df["description"] = df["description"].str.strip()
    return df

def create_and_save_icd10_df():
    df_cm = parse_icd10_raw_file(ICD10CM_RAW_PATH)
    df_pcs = parse_icd10_raw_file(ICD10PCS_RAW_PATH)
    df = pd.concat([df_cm, df_pcs], ignore_index=True)
    
    df["preprocessed_description"] = df["description"].apply(remove_stop_words_and_lemmatize)

    df.to_pickle(ICD10_DF_PATH)
    return df

def load_icd10_df():
    if not os.path.exists(ICD10_DF_PATH):
        return create_and_save_icd10_df()

    return pd.read_pickle(ICD10_DF_PATH)

def create_and_save_icd10_tfidf():
    df = load_icd10_df()
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(df["preprocessed_description"])

    with open(ICD10_TFIDF_PATH, 'wb') as f:
        pickle.dump((vectorizer, matrix), f)

    return vectorizer, matrix

def load_icd10_tfidf():
    if not os.path.exists(ICD10_TFIDF_PATH):
        return create_and_save_icd10_tfidf()

    with open(ICD10_TFIDF_PATH, 'rb') as f:
        vectorizer, matrix = pickle.load(f)
    
    return vectorizer, matrix