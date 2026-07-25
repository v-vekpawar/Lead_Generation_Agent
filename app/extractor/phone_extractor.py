import re

PHONE_PATTERNS = [
    r"\+\d{1,3}[\s-]?(?:\d[\s-]?){8,12}",  # international style
    r"\b[6-9]\d{9}\b",                     # indian style
    r"\b\d{2,4}[\s-]\d{6,8}\b"             # landline style
]

def extract_phone_numbers(text):
    phones=set()
    if not text:
        return []

    for pattern in PHONE_PATTERNS:
        matches = re.findall(pattern, text)

        for phone in matches:
            cleaned = phone.strip()
            phones.add(cleaned)

    return list(phones)