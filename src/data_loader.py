import os
import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from utils import remove_stop_words_and_lemmatize

ICD10_CSV_PATH = "data/icd10.csv"
ICD10_DF_PATH = "data/icd10_df.pickle"
ICD10_TFIDF_PATH = 'data/icd10_tfidf.pickle'

def preprocess_and_save_icd10_df():
    df = pd.read_csv(ICD10_CSV_PATH)
    df["WHO_Description_Preprocessed"] = df["WHO_Description"].apply(remove_stop_words_and_lemmatize)
    df.to_pickle(ICD10_DF_PATH)
    return df

def load_icd10_df():
    if not os.path.exists(ICD10_DF_PATH):
        return preprocess_and_save_icd10_df()

    return pd.read_pickle(ICD10_DF_PATH)

def generate_and_save_icd10_tfidf():
    df = load_icd10_df()
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(df["WHO_Description_Preprocessed"])

    with open(ICD10_TFIDF_PATH, 'wb') as f:
        pickle.dump((vectorizer, matrix), f)

    return vectorizer, matrix

def load_icd10_tfidf():
    if not os.path.exists(ICD10_TFIDF_PATH):
        return generate_and_save_icd10_tfidf()

    with open(ICD10_TFIDF_PATH, 'rb') as f:
        vectorizer, matrix = pickle.load(f)
    
    return vectorizer, matrix