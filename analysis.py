from langdetect import detect

def detect_lang(text: str) -> str:
    """
    Detects the language of the text and returns the language code.
    
    :param text: The text to be analyzed.
    :return: The language code of the text.
            NI if the language could not be detected.
    """
    try:
        return detect(text)
    except Exception:
        return 'NI'