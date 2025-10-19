"""
Test script for PDF parser
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from datasheet_parser.pdf_extractor import AutomotiveDatasheetParser, quick_extract


def test_parser(pdf_path: str):
    """Test the PDF parser with a sample datasheet"""
    
    print(f"\n{'='*60}")
    print(f"Testing PDF Parser: {pdf_path}")
    print(f"{'='*60}\n")
    
    # Test with context manager
    with AutomotiveDatasheetParser(pdf_path) as parser:
        # Print metadata
        print("📄 Document Metadata:")
        for key, value in parser.metadata.items():
            print(f"  {key}: {value}")
        
        # Extract first page as sample
        print("\n📖 Extracting Page 0 (First Page):")
        first_page = parser.extract_page_content(0)
        print(f"  Text length: {len(first_page['text'])} characters")
        print(f"  Tables found: {first_page['table_count']}")
        print(f"  Is register page: {first_page['is_register_page']}")
        
        if first_page['text'][:200]:
            print(f"\n  First 200 chars:\n  {first_page['text'][:200]}...")
        
        # Find register pages
        print("\n🔍 Searching for Register Pages:")
        register_pages = parser.extract_register_pages()
        print(f"  Found {len(register_pages)} pages with registers")
        
        if register_pages:
            print(f"\n  Sample Register Page (Page {register_pages[0]['page_number']}):")
            print(f"    Tables: {register_pages[0]['table_count']}")
            
            if register_pages[0]['tables']:
                table = register_pages[0]['tables'][0]
                print(f"    First table: {table['row_count']} rows × {table['column_count']} columns")
                print(f"    Headers: {table['headers']}")
        
        # Export to JSON
        output_path = "output/parsed_datasheet.json"
        Path("output").mkdir(exist_ok=True)
        parser.export_to_json(output_path)
        print(f"\n✅ Full extraction exported to: {output_path}")


if __name__ == "__main__":
    # Test with command line argument
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
    else:
        print("Usage: python test_pdf_parser.py <path_to_pdf>")
        print("\nPlease provide a sample automotive datasheet PDF")
        print("Example: python test_pdf_parser.py ../datasheets/TLE9189.pdf")
        sys.exit(1)
    
    test_parser(pdf_path)
