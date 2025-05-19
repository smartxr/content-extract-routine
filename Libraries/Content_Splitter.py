import os, re

# Read environment variable for max chunk size
MAX_CHUNK_SIZE = os.environ.get("MAX_CHUNK_SIZE", 5000)
# Check if the environment variable is set and is a valid integer
if MAX_CHUNK_SIZE is not None:
    try:
        MAX_CHUNK_SIZE = int(MAX_CHUNK_SIZE)
    except ValueError:
        MAX_CHUNK_SIZE = 5000

print(f"Max Chunk Size set to {MAX_CHUNK_SIZE}")


def split_large_content(text_content):
    # Split the text content into smaller chunks if it exceeds the maximum chunk size
    # Preference is to keep paragraphs together and split them only if they are too long

    if len(text_content) <= MAX_CHUNK_SIZE:
        # Text is small to keep as is. Convert to a List.
        return [text_content]

    # Text passed is too long. Split it into smaller chunks.
    text_chunks = []
    # First, break text by paragraphs
    paragraphs = text_content.split('\n')
    current_chunk = ""
    for paragraph in paragraphs:
        # If the paragraph is too long, split it into smaller chunks

        # Check is the paragraph is empty
        if len(paragraph.strip('\r').strip('\n').strip()) < 1:
            # Skip empty paragraphs
            continue

        # Check if the paragraph is more than size limit
        if len(paragraph) <= MAX_CHUNK_SIZE:
            # Check if accumulated text + current paragraph is within the limit
            if len(paragraph) + len(current_chunk) <= MAX_CHUNK_SIZE:
                current_chunk += paragraph + '\n'
            else:
                # Add the current chunk to the list of chunks
                text_chunks.append(current_chunk)
                # Reset the current chunk
                current_chunk = paragraph + '\n'

        # The current paragraph alone is larger than the limit
        else:
            # TODO: Check below if this is needed
            # # First, post any accumulated text
            # if len(current_chunk) > 0:
            #     # Add the current chunk to the list of chunks
            #     text_chunks.append(current_chunk)
            #     # Reset the current chunk
            #     current_chunk = ""

            # Split the paragraph into smaller chunks by sentences
            sentences = re.split(r'(?<=[.!?]) +', paragraph)
            for sentence in sentences:
                # Check if the sentence is too long
                if len(sentence) <= MAX_CHUNK_SIZE:
                    # Check if accumulated text + current sentence is within the limit
                    if len(sentence) + len(current_chunk) <= MAX_CHUNK_SIZE:
                        current_chunk += f'{sentence}.'
                    else:
                        # Add the current chunk to the list of chunks
                        text_chunks.append(current_chunk)
                        # Reset the current chunk
                        current_chunk = f'{sentence}.'
                else:
                    # If the sentence is too long, split it into smaller chunks
                    text_chunks.append(current_chunk)
                    current_chunk = ""

                    for i in range(0, len(sentence), MAX_CHUNK_SIZE):
                        chunk = sentence[i:i + MAX_CHUNK_SIZE]
                        text_chunks.append(chunk)


    # If there is any remaining text in the current chunk, add it to the list
    if len(current_chunk) > 0:
        text_chunks.append(current_chunk.strip('\n'))
        current_chunk = ""

    return text_chunks    

