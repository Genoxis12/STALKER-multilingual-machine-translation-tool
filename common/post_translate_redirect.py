from common.post_translate import french
import re

def post_translate_redirect(text, code):
    if code == "fr":
        return french.post_translation_ajust(text)
    
    # Use regex to replace specific patterns
    text = re.sub(r"\(\$+([A-Z_]+)\$+\)", r"($$\1$$)", text)

    # Other adjustments
    return (
        text
        .replace("%[defaut]", "%[default]")
        .replace("%[par defaut]", "%[default]")
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&apos;", "'")
        .replace("&#10;", "\n")
    )