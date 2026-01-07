import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_file, max_pages=50):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for i, page in enumerate(doc):
            if i >= max_pages:
                break
            text += page.get_text()
    return text
