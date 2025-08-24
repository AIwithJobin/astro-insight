from googletrans import Translator
_translator = Translator()

def translate(text: str, dest: str) -> str:
    if dest == "en":
        return text
    try:
        return _translator.translate(text, dest=dest).text
    except Exception:
        return text