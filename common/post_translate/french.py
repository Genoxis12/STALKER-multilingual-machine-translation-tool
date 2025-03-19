import re

def post_translation_ajust(text):
    # Utiliser une regex pour remplacer toutes les occurrences de ($ACTION_NAME$), ($$ACTION_NAME$), ou ($ACTION_NAME$$)
    text = re.sub(r"\(\$+([A-Z_]+)\$+\)", r"($$\1$$)", text)

    # Autres remplacements spécifiques
    return (
        text
        .replace("œ", "oe")
        .replace("%[defaut]", "%[default]")
        .replace("%[par defaut]", "%[default]")
        .replace("&amp;", "&")
    )