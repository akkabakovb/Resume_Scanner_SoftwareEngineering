import re


def sanitize_text(text: str) -> str:
    text = text.replace("\t", " ")
    text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E\x80-\xFF]", "", text)
    text = re.sub(r"\r\n|\r", "\n", text)
    return text
