def extract_document_name(file_path):

    if file_path.startswith("pdfs/") and file_path.endswith(".pdf"):
        document_name = file_path[len("pdfs/"):-len(".pdf")]
        return document_name

    return file_path
