import fitz  # aka PyMuPDF
import os


def main():
    # Set the path to your single PDF file
    pdf_path = "/path/to/your/file.pdf"  # Provide the path to the single PDF file
    extracted_text = convert_pdf_to_text(pdf_path)

    # Print the extracted text (or process further as needed)
    print(extracted_text)


def convert_pdf_to_text(pdf_path) -> str:
    """
    Extracts text from a single PDF file and returns it as a string.

    Parameters:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: A string containing the extracted text from the PDF.
    """
    # Ensure the file exists
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"The file at {pdf_path} was not found.")

    all_text = ""  # To hold the extracted text from the PDF

    # Extract text from the PDF
    with fitz.open(pdf_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            all_text += page.get_text()

    # Return the extracted text
    return all_text


if __name__ == "__main__":
    main()
