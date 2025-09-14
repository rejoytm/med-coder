import pytest
from src.icd_code_lookup import extract_icd10_codes
import pytest

@pytest.mark.parametrize("text, expected", [
    (
        # Single ICD-10-CM code
        "An example of an ICD-10-CM code is E11.9, which is common in adults.",
        ["E11.9"]
    ),
    (
        # No valid ICD-10 codes
        "No medical codes are mentioned here.",
        []
    ),
    (
        # Multiple ICD-10-CM codes
        "Another visit showed A09, A53, and Z00.129 symptoms",
        ["A09", "A53", "Z00.129"]
    ),
    (
        # Mix of ICD-10-CM and ICD-10-PCS codes
        "The patient presented with Z23.5 and H52.13. A procedure 0DTJ0ZZ was scheduled.",
        ["Z23.5", "H52.13", "0DTJ0ZZ"]
    ),
    (
        # Lowercase variations and some invalid entries
        "Conditions include j20 and 047K0ZZ, but not related to ABC123.",
        ["J20", "047K0ZZ"]
    ),
    (
        # Long text with mix of ICD-10-CM and ICD-10-PCS codes
        """
        The patient was diagnosed with E11.9 (Type 2 diabetes mellitus without complications) 
        and H52.13 (Myopia), along with Z23.5 (Encounter for immunization). Another commonly 
        documented condition is Z00.129 (Routine child health exam without abnormal findings), 
        and A53 (Late syphilis) may also be observed during routine visits. Other possibilities, 
        such as A09 (Infectious gastroenteritis) or J20 (Acute bronchitis), were considered 
        but ruled out. Additional findings included S72.001A (Fracture of the right femur, 
        initial encounter). Procedure examples include 0DTJ0ZZ and 047K0ZZ.
        """,
        ["E11.9", "H52.13", "Z23.5", "Z00.129", "A53", "A09", "J20", "S72.001A", "0DTJ0ZZ", "047K0ZZ"]
    )
])
def test_extract_icd10_codes(text, expected):
    result = extract_icd10_codes(text)
    assert sorted(result) == sorted(expected)
