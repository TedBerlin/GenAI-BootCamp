from pypdf import PdfReader
import cleaner

# ---------------- PDF ----------------
def extract_text_from_pdf(uploaded_file) -> str:
    uploaded_file.seek(0)
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return cleaner.clean_text(text)