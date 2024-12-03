from pypdf import PdfReader
import os
import scanner

def parse_pdf(file_path, output_path):
    """
    Parse PDF file and extract text with improved handling of formatting and layout.
    
    Args:
        file_path (str): Path to the input PDF file
        output_path (str): Path to save the extracted text file
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        # Open the PDF file
        pdf = PdfReader(file_path)
        
        # Open output text file
        with open(output_path, 'w', encoding='utf-8') as f:
            # Process each page
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract text from the page
                page_text = page.extract_text()
                
                # Remove excessive whitespace and clean up text
                cleaned_text = ' '.join(page_text.split())
                
                # Write page content with page number as header
                # f.write(f"GISC4317 Course Syllabus Page {page_num}\n")
                f.write(cleaned_text + '\n\n')
                
        print(f"Successfully converted PDF to text: {output_path}")
    
    except Exception as e:
        print(f"Error converting PDF: {e}")

def main():
    # Paths for input PDF and output text file
    
    pdf_path = '../uploads/4317Syllabus-chastain2.pdf'
    output_txt_path = '../uploads/sample.txt'
    
    # Convert PDF to text
    parse_pdf(pdf_path, output_txt_path)

    # Extract important dates from the text
    important_dates = scanner.extract_dates_from_syllabus(output_txt_path)
    
    # Print the extracted dates
    for date_info in important_dates:
        print(f"Date: {date_info['date']}, Context: {date_info['context']}")

    
if __name__ == '__main__':
    main()
