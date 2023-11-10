def read_file(file_path):
    """
    Reads the entire content of a file and returns it as a string.
    """
    with open(file_path, "r") as file:
        return file.read()


def chunk_text_by_paragraphs(text):
    """
    This function takes a string of text and returns a list of paragraphs.
    A paragraph is defined as a string of text that is separated by two or more newlines.
    """
    # Split the text by two or more newlines to separate paragraphs
    paragraphs = text.split("\n\n")

    # Filter out any empty strings that may result from extra newlines
    paragraphs = [para.strip() for para in paragraphs if para.strip()]

    return paragraphs


def chunk_file(file_path):
    """
    This function takes a file path, reads the file, and chunks it into paragraphs.
    It returns an array of paragraphs.
    """
    # Read the content of the file
    text_content = read_file(file_path)

    # Chunk the text by paragraphs
    paragraphs = chunk_text_by_paragraphs(text_content)

    return paragraphs
