import re

# Collapses multiple whitespace characters into a single space and removes leading/trailing whitespace
def collapse_and_strip_whitespace(string):
    return re.sub(r'\s+', ' ', string).strip()