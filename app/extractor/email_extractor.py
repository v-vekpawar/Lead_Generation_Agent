import re
from typing import List

EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", re.IGNORECASE,)

PLACEHOLDER_EMAILS = {"example@example.com", "email@example.com", "your@email.com",}

def clean_email(email: str) -> str:
    """Normalize a raw email candidate"""

    email = email.strip()
    for prefix in ("mailto:", "MAILTO:", "javascript:"):
        if email.lower().startswith(prefix.lower()):
            email = email[len(prefix):]

    email = email.strip("\t\r\n<>\"'`()[]{}.,;:/\\")

    email = re.sub(r"^\d{8,15}(?=[A-Za-z])", "", email)

    return email.lower()

def is_valid_email(email: str) -> bool:
    """Basic sanity validation"""

    if not email:
        return False
    
    if email in PLACEHOLDER_EMAILS:
        return False

    if email.count("@") != 1:
        return False

    if " " in email:
        return False

    if ".." in email:
        return False

    if email.startswith(("http://", "https://")):
        return False

    local, domain = email.split("@")

    if "." not in domain:
        return False

    if not local or not domain:
        return False

    if domain.startswith(".") or domain.endswith("."):
        return False

    return EMAIL_PATTERN.fullmatch(email) is not None

def extract_emails(text: str, links: List[str] | None = None) -> List[str]:
    """Extract, clean, validate and deduplicate email addresses."""

    candidates = []

    if text:
        candidates.extend(EMAIL_PATTERN.findall(text))

    if links:
        for link in links:
            if link.lower().startswith("mailto:"):
                candidates.append(link)

    emails = []
    seen = set()

    for candidate in candidates:
        email = clean_email(candidate)
        if not is_valid_email(email):
            continue
        if email in seen:
            continue
        seen.add(email)
        emails.append(email)

    return emails