import re

EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

def extract_emails(text, links=None):
    emails = set()
    if text:
        found = EMAIL_PATTERN.findall(text)
        emails.update(found)

    if links:
        for link in links:
            if link.startswith("mailto:"):
                email = link.replace("mailto:","")
                emails.add(email)

    return list(emails)