import re


def clean_text(
    value: str,
) -> str:
    pattern = r'([\\/:*?"<>|,])'
    # remove special characters
    cleaned_text = re.sub(pattern, "", value)
    # remove multiple spaces
    cleaned_text = re.sub(r"\s+", " ", cleaned_text)
    return cleaned_text.strip()
