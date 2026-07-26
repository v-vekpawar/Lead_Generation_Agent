import re
from typing import List

PHONE_PATTERNS = [
    r"\+\d{1,3}[\s-]?(?:\d[\s-]?){8,12}",
    r"\b[6-9]\d{9}\b",
    r"\b\d{2,4}[\s-]\d{6,8}\b",
]

def normalize_phone(phone: str) -> str:
    """Normalize phone numbers while preserving international numbers."""

    phone = phone.strip()
    phone = re.sub(r"(?!^\+)[^\d]", "", phone)

    if phone.startswith("+91"):
        digits = phone[3:]
        if len(digits) == 10:
            return digits
        return ""

    if phone.startswith("91") and len(phone) == 12:
        return phone[2:]

    if phone.startswith("+"):
        return phone

    return phone

def extract_phones(text: str) -> List[str]:
    if not text:
        return []

    phones = []
    seen = set()

    for pattern in PHONE_PATTERNS:
        matches = re.findall(pattern, text)
        for phone in matches:
            normalized = normalize_phone(phone)
            if not normalized:
                continue
            if normalized in seen:
                continue
            seen.add(normalized)
            phones.append(normalized)

    return phones