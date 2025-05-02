import logging

from lxml.html import HtmlElement, fragments_fromstring

logger = logging.getLogger("uvicorn")


def sanitize_dict(data: dict) -> dict:
    keys_to_be_sanitized = [
        "GestartBeëindigdTitel",
        "KostenCategorieTitel",
        "DoorlooptijdAantallenTitel",
        "DoorlooptijdwijzigingRedenenTitel",
        "DashboardKop",
        "GewijzifdeIctActiviteiten",
        "StatusverdelingTitel",
        "SchattingTotaleKostenTitel",
        "GrafiekKostenCategorie",
        "kostenTotaalStelselTitel",
        "kostenTotaalKV",
        "kostenTotaalBL",
    ]

    for key in data.keys():
        value = data[key]
        if isinstance(value, dict):
            data[key] = sanitize_dict(value)
        elif key in keys_to_be_sanitized:
            parsed_value = fragments_fromstring(html=value, no_leading_text=False)
            data[key] = "".join(
                [p.text if type(p) is HtmlElement else p for p in parsed_value]
            )
        else:
            data[key] = value
    return data
