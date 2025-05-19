import os, re, json, base64
from datetime import datetime, timezone
import Libraries.Content_Splitter as content_splitter


# Encode a line of text to Base64
def encode_filename(file_name):
    # Convert the filename to bytes
    file_name_bytes = file_name.encode('utf-8')
    # Encode the bytes to base64
    base64_bytes = base64.b64encode(file_name_bytes)
    # Convert the base64 bytes back to a string
    file_name_base64 = base64_bytes.decode('utf-8')
    return file_name_base64


# Create output folder based on the source file name
def create_output_folder(full_file_name, produced_folder):
    # Get the file name without the file path
    file_name = os.path.basename(full_file_name)

    # Encode the file name to Base64 and assign it to the folder name
    folder_name_base64 = encode_filename(file_name)

    # Setup output folder based on Base64 encodded file name
    output_folder = os.path.join(produced_folder, folder_name_base64)
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Return the output folder path
    return output_folder, file_name


def get_file_title(file_name: str) -> str:
    # Convert string into separate words.

    # Option 1:
    # Underscore, dash, dot, space or transitioning from small to capital letters will constitute a start of a new word.
    # # There might be multiple words in the input string.
    # pattern = r'[_.\-\s]+|(?<=[a-z])(?=[A-Z])'  # Alternative pattern: r'[_\- ]|(?<=[a-z])(?=[A-Z])'
    # words = re.split(pattern, os.path.splitext(file_name)[0])
    # return ' '.join(words)

    # Option 2:
    # Underscore, dash, space, transitioning from small to capital letters, from numbers to letters and wise versa will constitute a start of a new word.
    # # Replace underscores, dashes, and spaces with a space
    # cleaned = re.sub(r'[_\-\s]+', ' ', input_string)
    # # Split words at transitions:
    # # - lower to upper (e.g., camelCase -> camel Case)
    # # - letter to digit and digit to letter (e.g., word123 -> word 123)
    # split_pattern = r'(?<=[a-z])(?=[A-Z])|(?<=[A-Za-z])(?=\d)|(?<=\d)(?=[A-Za-z])'

    # # Split each token further based on above transitions
    # words = []
    # for token in cleaned.split():
    #     words.extend(re.split(split_pattern, token))

    # return ' '.join(words)

    # Option 3:
    # # Step 1: Replace all separators with spaces
    # normalized = re.sub(r'[_\-\s]+', ' ', input_string)
    
    # # Step 2: Insert spaces at transitions:
    # # - lowerCase -> lower Case
    # # - digitLetter -> digit Letter
    # # - letterDigit -> letter Digit
    # spaced = re.sub(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Za-z])(?=\d)|(?<=\d)(?=[A-Za-z])', ' ', normalized)

    # # Step 3: Normalize multiple spaces and strip leading/trailing space
    # cleaned = re.sub(r'\s+', ' ', spaced).strip()
    
    # return cleaned

    # Option 4:
    # Underscore, dash, space, dot, transitioning from small to capital letters, from numbers to letters and wise versa will constitute a start of a new word.
    # Step 1: Replace common separators with a space
    normalized = re.sub(r'[_\-\+\s]+', ' ', os.path.splitext(file_name)[0])
    # Step 2: Insert space before transitions:
    # a) lowercase to uppercase (e.g., myWord -> my Word)
    # b) letter to digit or digit to letter (e.g., Word2Go -> Word 2 Go)
    # normalized = re.sub(r'([a-z])([A-Z])', r'\1 \2', normalized)
    # normalized = re.sub(r'([A-Za-z])(\d)', r'\1 \2', normalized)
    # normalized = re.sub(r'(\d)([A-Za-z])', r'\1 \2', normalized)

    normalized = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', normalized)  # camelCase: aA
    normalized = re.sub(r'(?<=[A-Za-z])(?=[0-9])', ' ', normalized)      # letterNumber: a1
    normalized = re.sub(r'(?<=[0-9])(?=[A-Za-z])', ' ', normalized)      # numberLetter: 1a

    # Step 3: Normalize multiple spaces and strip leading/trailing whitespace
    return ' '.join(normalized.strip().split())


def write_content_to_json_file(text_content, target_folder, source_file_name, file_name, page_number_ref, image_index_ref=0):
    file_title = get_file_title(file_name)

    # Split text into chunks
    text_chunks = content_splitter.split_large_content(text_content)
    # text_chunks = [text_content]
    
    chunk_id_ref = 0
    for text_chunk in text_chunks:
        chunk_id_ref += 1

        # Build proper JSON file structure
        json_object = {
            "url": source_file_name,
            "filename": file_name,
            "page_number": page_number_ref,
            "image_index": image_index_ref,
            "chunk_id": chunk_id_ref,
            "title": file_title,
            "content": text_chunk,
            "last_updated": datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"),
            "keywords": "",
            "vectors": "",
        }

        # Build target file name
        if image_index_ref < 1:
            target_file_name = f'Page_{str(page_number_ref).zfill(4)}_Chunk_{str(chunk_id_ref).zfill(3)}.json'
        else:
            target_file_name = f'Page_{str(page_number_ref).zfill(4)}_Image_{str(image_index_ref).zfill(3)}_Chunk_{str(chunk_id_ref).zfill(3)}.json'


        target_full_file_name = os.path.join(target_folder, target_file_name)

        # Convert the content to JSON format
        # json_content = json.dumps(json_object, indent=4)

        # Write the JSON content to a file
        with open(target_full_file_name, 'w', encoding='utf-8') as file:
            json.dump(json_object, file, ensure_ascii=False)
            # json.dump(json_object, file, ensure_ascii=False, indent=4)
            # file.write(json_content)

        print("Content written to ", target_full_file_name)

