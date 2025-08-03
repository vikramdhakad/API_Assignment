from translate import Translator


def translate_text(text, target_lang="hi"):
    try:
        translator = Translator(to_lang=target_lang)
        return translator.translate(text)
    except Exception as e:
        return f"Translation Error: {str(e)}"