from pypdf import PdfReader
import os
import logging
import scanner

def parse_pdf(file_path, output_path):
    """
    Parse PDF file and extract text with improved handling of formatting and layout.
    
    Args:
        file_path (str): Path to the input PDF file
        output_path (str): Path to save the extracted text file
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Open the PDF file
        pdf = PdfReader(file_path)
        
        # Open output text file
        with open(output_path, 'w', encoding='utf-8') as f:
            # Process each page
            for page_num, page in enumerate(pdf.pages, 1):
                # Extract text from the page
                page_text = page.extract_text()
                
                # More sophisticated text cleaning
                # Remove excessive whitespace while preserving some formatting
                lines = [line.strip() for line in page_text.split('\n') if line.strip()]
                cleaned_text = '\n'.join(lines)
                
                # Write page content
                f.write(f"--- Page {page_num} ---\n")
                f.write(cleaned_text + '\n\n')
                
        logger.info(f"Successfully converted PDF to text: {output_path}")
        return output_path
    
    except Exception as e:
        logger.error(f"Error converting PDF: {e}")
        raise

def main():
    """
    Example usage and testing of PDF parsing
    """
    try:
        # Paths for input PDF and output text file
        pdf_path = '../uploads/4317Syllabus-chastain2.pdf'
        output_txt_path = '../uploads/sample.txt'
        
        # Convert PDF to text
        parsed_file = parse_pdf(pdf_path, output_txt_path)

        # Extract important dates from the text
        important_dates = scanner.extract_dates_from_syllabus(parsed_file)
        
        # Print the extracted dates
        print("Extracted Important Dates:")
        for date_info in important_dates:
            print(f"Date: {date_info['date']}, Context: {date_info['context']}")
    
    except Exception as e:
        logging.error(f"Error in main processing: {e}")

if __name__ == '__main__':
    main()