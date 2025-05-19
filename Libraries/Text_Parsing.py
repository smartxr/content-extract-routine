import Libraries.Write_Files as write_files


def parse_plain_text_content(full_file_name, produced_folder):
    # Read the content of a text file
    with open(full_file_name, 'r', encoding='utf-8') as file:
        extracted_text = file.read()

    # Get output folder for the produced content
    output_folder, file_name = write_files.create_output_folder(full_file_name, produced_folder)

    # Save result to JSON file
    # Content will be chopped down to maximum size
    write_files.write_content_to_json_file(extracted_text, output_folder, full_file_name, file_name, page_number_ref=1)


# Testing the module
if __name__ == "__main__":
    # Example usage
    produced_folder = r"c:\Users\Eugene\Downloads\Materials\Produced"
    full_file_name = r"c:\Users\Eugene\Downloads\Materials\Sources\Microsoft_365_Copilot_Boot_Camp_(Day_3_of_3)_(4420555)_Part_1.srt"
    parse_plain_text_content(full_file_name, produced_folder)