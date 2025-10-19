"""
PDF Datasheet Parser for Automotive Documents
Extracts text and structured tables from technical datasheets
"""

import fitz  # PyMuPDF
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json

class RectEncoder(json.JSONEncoder):
    """Custom JSON encoder for PyMuPDF Rect objects"""
    def default(self, obj):
        if isinstance(obj, fitz.Rect):
            return {
                "x0": obj.x0,
                "y0": obj.y0,
                "x1": obj.x1,
                "y1": obj.y1,
                "width": obj.width,
                "height": obj.height
            }
        return super().default(obj)


class AutomotiveDatasheetParser:
    """
    Specialized parser for automotive component datasheets.
    Handles register maps, timing diagrams, electrical characteristics.
    """
    
    def __init__(self, pdf_path: str):
        """Initialize parser with PDF path"""
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        
        self.doc = fitz.open(str(self.pdf_path))
        self.metadata = self._extract_metadata()
        
    def _extract_metadata(self) -> Dict:
        """Extract PDF metadata (title, author, page count)"""
        return {
            "filename": self.pdf_path.name,
            "page_count": len(self.doc),
            "title": self.doc.metadata.get("title", ""),
            "author": self.doc.metadata.get("author", ""),
            "subject": self.doc.metadata.get("subject", "")
        }
    
    def extract_page_content(self, page_num: int) -> Dict:
        """
        Extract all content from a specific page
        
        Args:
            page_num: Page number (0-indexed)
            
        Returns:
            Dictionary with text, tables, and metadata
        """
        if page_num >= len(self.doc):
            raise ValueError(f"Page {page_num} out of range (max: {len(self.doc)-1})")
        
        page = self.doc[page_num]
        
        # Extract text
        text = page.get_text("text")
        
        # Extract tables
        tables = self._extract_tables_from_page(page)
        
        # Detect if page contains register information
        is_register_page = self._is_register_page(text)
        
        return {
            "page_number": page_num,
            "text": text,
            "tables": tables,
            "table_count": len(tables),
            "is_register_page": is_register_page,
            "page_size": tuple(page.rect)
        }
    
    def _extract_tables_from_page(self, page) -> List[Dict]:
        """
        Extract tables using PyMuPDF's table detection
        
        Returns:
            List of tables, each as a dict with headers and rows
        """
        tables_data = []
        
        # Find all tables on the page
        tables = page.find_tables()
        
        if not tables:
            return []
        
        for table_idx, table in enumerate(tables):
            # Extract table as pandas DataFrame for easy manipulation
            df = table.to_pandas()
            
            # Convert to dict format
            table_dict = {
                "table_id": table_idx,
                "row_count": len(df),
                "column_count": len(df.columns),
                "headers": df.columns.tolist() if not df.empty else [],
                "rows": df.values.tolist() if not df.empty else [],
                "bbox": tuple(table.bbox),  # Bounding box coordinates
            }
            
            tables_data.append(table_dict)
        
        return tables_data
    
    def _is_register_page(self, text: str) -> bool:
        """
        Detect if page contains register information
        Common keywords in automotive datasheets
        """
        register_keywords = [
            "register", "bit field", "address", "offset",
            "read/write", "reset value", "0x", "bit[",
            "configuration", "status register", "control register"
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in register_keywords)
    
    def extract_register_pages(self) -> List[Dict]:
        """
        Extract only pages containing register information
        Useful for automotive datasheets where registers are key
        """
        register_pages = []
        
        for page_num in range(len(self.doc)):
            content = self.extract_page_content(page_num)
            if content["is_register_page"] and content["table_count"] > 0:
                register_pages.append(content)
        
        return register_pages
    
    def extract_all_content(self) -> Dict:
        """
        Extract complete document content
        """
        all_pages = []
        
        for page_num in range(len(self.doc)):
            all_pages.append(self.extract_page_content(page_num))
        
        return {
            "metadata": self.metadata,
            "pages": all_pages,
            "total_pages": len(all_pages),
            "register_page_count": sum(1 for p in all_pages if p["is_register_page"])
        }
    
    def export_to_json(self, output_path: str):
        """Export extracted content to JSON"""
        content = self.extract_all_content()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False, cls=RectEncoder)
        
        print(f"Exported to: {output_path}")
    
    def close(self):
        """Close the PDF document"""
        self.doc.close()
    
    def __enter__(self):
        """Context manager support"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup"""
        self.close()


# Convenience function for quick extraction
def quick_extract(pdf_path: str) -> Dict:
    """
    Quick extraction of register pages from automotive datasheet
    
    Usage:
        data = quick_extract("TLE9189_datasheet.pdf")
    """
    with AutomotiveDatasheetParser(pdf_path) as parser:
        return parser.extract_register_pages()
