import medspacy
from medspacy.section_detection import SectionRule

from utils import collapse_and_strip_whitespace

sectionizer_nlp = medspacy.load(medspacy_enable=["medspacy_sectionizer"], load_rules=False)

section_rules = [
    # Chief Complaint
    SectionRule(literal="Chief Complaint", category="chief_complaint"),
    SectionRule(literal="CC", category="chief_complaint"), 
    
    # History of Present Illness
    SectionRule(literal="History of Present Illness", category="history_of_present_illness"),
    SectionRule(literal="HPI", category="history_of_present_illness"),

    # Subjective
    SectionRule(literal="Subjective", category="subjective"),     

    # Review of Systems    
    SectionRule(literal="Review of Systems", category="review_of_systems"),    
    SectionRule(literal="Review of Symptoms", category="review_of_systems"),    
    
    # Medical History
    SectionRule(literal="Past Medical History", category="medical_history"),    
    SectionRule(literal="Medical History", category="medical_history"),        
    SectionRule(literal="Past History", category="medical_history"),
    
    # Surgical History
    SectionRule(literal="Past Surgical History", category="surgical_history"),    
    SectionRule(literal="Surgical History", category="surgical_history"),   

    # Family History
    SectionRule(literal="Family History", category="family_history"),   

    # Social History
    SectionRule(literal="Social History", category="social_history"),

    # Allergies
    SectionRule(literal="Allergies", category="allergies"), 
   
    # Current Medications
    SectionRule(literal="Current Medications", category="medications"),      
    SectionRule(literal="Medications", category="medications"),  

    # Vitals
    SectionRule(literal="Vitals Reviewed", category="vitals"),      
    SectionRule(literal="Vitals", category="vitals"),    

    # Physical Examination
    SectionRule(literal="Physical Examination", category="physical_examination"),  
    SectionRule(literal="Physical Exam", category="physical_examination"),  
    SectionRule(literal="Exam", category="physical_examination"),

    # Results
    SectionRule(literal="Results", category="results"),    

    # Assessment and Plan
    SectionRule(literal="Assessment and Plan", category="assessment_and_plan"),    
    SectionRule(literal="Assessment", category="assessment_and_plan"),    
    SectionRule(literal="Plan", category="assessment_and_plan"),

    # Impression
    SectionRule(literal="Impression", category="impression"),

    # Instructions
    SectionRule(literal="Instructions", category="instructions"),
]

sectionizer_nlp.get_pipe("medspacy_sectionizer").add(section_rules)

# Parses raw clinical notes into distinct SOAP sections and returns them as a dictionary
def sectionize_soap_note(text):
    doc = sectionizer_nlp(text)

    """
    medspaCy uses section rules (e.g., "Plan") to sectionize the document. However, these keywords 
    may appear multiple times in clinical notes, causing incorrect section splits. To mitigate this, 
    we keep the first occurrence of each section and ignore subsequent ones, assuming the first 
    detection is correct.
    
    This approach works in most cases but may result in false positives. 
    TODO: Implement a more reliable method for detecting incorrect section splits.
    """    

    soap_sections = {}
    prev_section_category = None

    for section in doc._.sections:
        body = collapse_and_strip_whitespace(str(doc[section.body_span[0]:section.body_span[1]]))
        
        if section.category in soap_sections: # Keyword wrongly detected as section start
            keyword = collapse_and_strip_whitespace(str(doc[section.title_span[0]:section.title_span[1]]))
            soap_sections[prev_section_category] += f" {keyword} {body}"
        else: # First occurence of this section category
            soap_sections[section.category] = body
            prev_section_category = section.category

    return soap_sections