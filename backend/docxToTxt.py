from docx import Document

def parse_docx(file_path,output_path):
    doc = Document(file_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        for para in doc.paragraphs:
            f.write(para.text, '\n')