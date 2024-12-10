from docx import Document
import logging

def parse_docx(file_path, output_path):
    """
    Convert a DOCX file to a plain text file.
    
    Args:
        file_path (str): Path to the input DOCX file
        output_path (str): Path to save the extracted text file
    """
    try:
        # Open the Word document
        doc = Document(file_path)
        
        # Open output text file
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write paragraphs, ensuring each paragraph is on a new line
            for para in doc.paragraphs:
                # Only write non-empty paragraphs
                if para.text.strip():
                    f.write(para.text + '\n')
        
        print(f"Successfully converted DOCX to text: {output_path}")
    
    except Exception as e:
        logging.error(f"Error converting DOCX: {e}")
        raise