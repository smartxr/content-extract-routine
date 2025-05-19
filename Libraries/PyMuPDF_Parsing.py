import re
import pymupdf
import Libraries.OCR_Image as ocr_image
import Libraries.Write_Files as write_files

# Parse the content with PyMuPDF.
def parse_pymupdf_content(full_file_name, produced_folder):
    print("PyMuPDF parsing module in use.")
    document_object = pymupdf.open(full_file_name)

    # Get output folder for the produced content
    output_folder, file_name = write_files.create_output_folder(full_file_name, produced_folder)

    # Get the number of pages in the document
    print(len(document_object), " pages")
    print(document_object.page_count, " pages")

    # Iterate through each page
    for page_number in range(document_object.page_count):
        # --------===== SECTION : PAGE =====--------
        # Get the page object; Page number
        page = document_object[page_number]
        page_number_ref = page_number + 1
        print("Page ", page_number_ref)

        # --------===== SECTION : TEXT =====--------
        # Extract text from the page
        # text = page.get_text()
        # chunk_id = 0
        text_lines = []
        for block in page.get_text("blocks", sort=False):
            text = re.sub(r'[\n\r]', '', block[4])
            text_lines.append(text)
            # print(text)

        full_text = '\n'.join(text_lines)
        write_files.write_content_to_json_file(full_text, output_folder, full_file_name, file_name, page_number_ref)


        # --------===== SECTION : IMAGES =====--------
        # Get images on the page
        image_list = page.get_images(full=True)
        # Check if there are images on the page
        if image_list:
            # printing number of images found in this page
            print(f"Page {page_number_ref} has {len(image_list)} images")

            for image_index, img in enumerate(image_list, start=1):
                # get the XREF of the image
                xref = img[0]
                image_index_ref = image_index + 1

                # extract the image bytes
                base_image = document_object.extract_image(xref)
                image_bytes = base_image["image"]

                # Run OCR on the image bytes
                extracted_text = ocr_image.ocr_file(image_bytes)

                # Check if the extracted text is empty
                # Trimming spaces, new lines, tabs and other non-printable characters
                extracted_text = extracted_text.strip('\r').strip('\n').strip('\t').strip()
                # Assuming text under 10 charecters is not useful
                if len(extracted_text) < 10:
                    print(f"Page {page_number_ref} Image {image_index}: No text found.")
                else:
                    # Print the text content
                    print(f"Page {page_number_ref} Image {image_index}:\n{extracted_text}\n")

                    # Save result to a file
                    write_files.write_content_to_json_file(extracted_text, output_folder, full_file_name, file_name, page_number_ref, image_index_ref)


# Testing the module
if __name__ == "__main__":
    # Example usage
    produced_folder = r"c:\Users\Eugene\Downloads\Materials\Produced"
    full_file_name = r"c:\Users\Eugene\Downloads\Materials\Sources\faa-h-8083-25c (Pilot’s Handbook of Aeronautical Knowledge).pdf"
    parse_pymupdf_content(full_file_name, produced_folder)
