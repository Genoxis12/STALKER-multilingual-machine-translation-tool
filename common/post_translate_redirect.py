from post_translate import french

def post_translate_redirect(text, code):
    if code == "fr":
        return french.post_translation_adjust(text)
    return text