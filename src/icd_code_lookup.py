import re

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