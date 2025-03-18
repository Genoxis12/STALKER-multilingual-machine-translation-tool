from .. languages import LANGUAGE_INPUT_TEXT, LANGUAGES_CONF
import os
import xml.etree.ElementTree as ET

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
                print(string_element)
                return False
        return True
    except ET.ParseError as e:
        print(f"Error parsing XML file: {file_path}")
        print(e)
        return False


def process_folder(folder_path):
    # Create a new folder for translated files at the same level as the input folder
    parent_folder = os.path.dirname(folder_path)
    output_folder = os.path.join(parent_folder, "translated_files")
    os.makedirs(output_folder, exist_ok=True)

    total_files = 0
    validated_files = 0
    files_errors = 0

    # Iterate through all files in the folder
    for root, _, files in os.walk(folder_path):
        for file in files:
            total_files += 1
            file_path = os.path.join(root, file)

            if file.endswith(".xml"):  # Process only XML files
                print(f"Checking XML file format: {file_path}")
                if is_valid_xml(file_path):  # Validate XML format
                    print(f"Valid file : {file_path}")
                    validated_files += 1
                else:
                    print(f"Skipped invalid XML file: {file_path}")
                    files_errors += 1
    
    return total_files, validated_files, files_errors


folder_path = get_folder_path()

total_files, validated_files, files_errors = process_folder(folder_path)

print("===============================================")
print("summary")
print("-----------------------------------------------")
print(f"Total files: {total_files}")
print(f"Validated files: {validated_files}")
print(f"Files with errors: {files_errors}")
print("===============================================")