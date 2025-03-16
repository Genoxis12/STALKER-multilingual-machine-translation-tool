import os
import shutil
import xml.etree.ElementTree as ET
import deepl
import unicodedata
from common.api import API_KEY
from common.languages import LANGUAGES_CONF, LANGUAGE_INPUT_TEXT


def get_language_code():
    print(LANGUAGE_INPUT_TEXT)
    while True:
        selected_lang = input("Enter the language code: ").upper()
        if selected_lang in LANGUAGE_INPUT_TEXT:
            return selected_lang
        print("Invalid language code. Please try again.")


def get_folder_path(language_code="EN"):
    folder_path = input(f"{LANGUAGES_CONF[language_code]['select_folder_text']}")
    while not os.path.exists(folder_path):
        print(LANGUAGES_CONF[language_code]['folder_not_found'])
        folder_path = input(f"{LANGUAGES_CONF[language_code]['select_folder_text']}")
    return folder_path


def translate_text(text, translator, target_lang="EN"):
    translated = translator.translate_text(text, target_lang=target_lang).text
    # Remove accents from the translated text
    normalized = unicodedata.normalize('NFD', translated)
    text_without_accents = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    return text_without_accents


def is_valid_xml(file_path):
    """
    Check if the XML file has the correct format:
    - Contains <string> elements with <text> sub-elements that have content.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Check if all <string> elements have a <text> sub-element with content
        for string_element in root.findall(".//string"):
            text_element = string_element.find("text")
            if text_element is None or not text_element.text.strip():
                print(f"Invalid format in file: {file_path}")
                return False
        return True
    except ET.ParseError:
        print(f"Error parsing XML file: {file_path}")
        return False


def process_xml(file_path, translator, output_folder, target_lang="EN"):
    print("===============================================")
    print(f"Translating XML file: {file_path}")
    print("===============================================")
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Iterate through all <string> elements and translate their <text> sub-elements
    for string_element in root.findall(".//string"):
        text_element = string_element.find("text")
        if text_element is not None and text_element.text:  # Ensure <text> exists and has content
            translated_text = translate_text(text_element.text, translator, target_lang=target_lang)
            text_element.text = translated_text
            print(f"Translated: {text_element.text}")

    # Save the modified XML to the output folder
    output_file = os.path.join(output_folder, os.path.relpath(file_path, folder_path))
    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure subdirectories exist
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Translated XML saved to: {output_file}")
    print("===============================================")


def update_localization_file(folder_path, localisation_code="eng"):
    """
    Check if localization.ltx exists and update it to include the localization code in the language line.
    """
    localization_file = os.path.join(folder_path, "localization.ltx")
    if os.path.exists(localization_file):
        print(f"Updating {localization_file} to include {localisation_code} in the language line.")
        with open(localization_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open(localization_file, "w", encoding="utf-8") as file:
            for line in lines:
                if line.strip().startswith("language"):
                    if "fra" not in line:
                        line = line.strip() + f" ;{localisation_code}\n"
                file.write(line)
        print(f"Updated {localization_file} successfully.")
    else:
        print(f"No localization.ltx file found in {folder_path}.")


def process_folder(folder_path, translator, target_lang="EN"):
    # Create a new folder for translated files at the same level as the input folder
    parent_folder = os.path.dirname(folder_path)
    output_folder = os.path.join(parent_folder, "translated_files")
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all files in the folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder_path)  # Preserve relative path
            output_file_path = os.path.join(output_folder, relative_path)

            if file.endswith(".xml"):  # Process only XML files
                print(f"Checking XML file format: {file_path}")
                if is_valid_xml(file_path):  # Validate XML format
                    print(f"Processing XML file: {file_path}")
                    process_xml(file_path, translator, output_folder, target_lang=target_lang)
                else:
                    print(f"Skipped invalid XML file: {file_path}")
            else:
                # Copy non-XML files to the output folder, preserving structure
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
                shutil.copy(file_path, output_file_path)
                print(f"Copied non-XML file: {file_path}")

    # Move translated files to gamedata\configs\text\fra if localization.ltx exists
    gamedata_text_folder = os.path.join(folder_path, "gamedata", "configs", "text", LANGUAGES_CONF[target_lang]["localization_code"])
    if os.path.exists(os.path.join(folder_path, "localization.ltx")):
        os.makedirs(gamedata_text_folder, exist_ok=True)
        for root, _, files in os.walk(output_folder):
            for file in files:
                src_file = os.path.join(root, file)
                relative_path = os.path.relpath(src_file, output_folder)
                dest_file = os.path.join(gamedata_text_folder, relative_path)
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                shutil.move(src_file, dest_file)
        print(f"Translated files moved to: {gamedata_text_folder}")

    # Update localization.ltx
    update_localization_file(folder_path, localisation_code=LANGUAGES_CONF[target_lang]["localization_code"])

    print(f"All files processed. Translated files are in: {output_folder}")


# Main script
if __name__ == "__main__":
    language_code = get_language_code()
    folder_path = get_folder_path(language_code=language_code)

    auth_key = API_KEY
    translator = deepl.Translator(auth_key)

    process_folder(folder_path, translator, target_lang=language_code)