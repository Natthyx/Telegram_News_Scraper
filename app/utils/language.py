import langid # type: ignore

def detect_language(text: str) -> str:
    try:
        lang , _ = langid.classify(text)
        return lang
    except Exception:
        return "unknown"
    