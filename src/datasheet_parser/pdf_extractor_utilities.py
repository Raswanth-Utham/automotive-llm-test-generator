"""
Enhanced utility functions for page-range-based extraction
Add these functions to your test_llm_integration.py or create a new utils.py file
"""
from pathlib import Path
import sys
# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json
from .pdf_extractor import AutomotiveDatasheetParser


def extract_specific_pages(
    parser: 'AutomotiveDatasheetParser',
    page_numbers: List[int]
) -> List[Dict]:
    """
    Extract content from specific page numbers
    
    Args:
        parser: Instance of AutomotiveDatasheetParser
        page_numbers: List of page numbers (0-indexed) to extract
        
    Returns:
        List of page content dictionaries
        
    Example:
        pages = extract_specific_pages(parser, [10, 15, 20, 25])
    """
    extracted_pages = []
    
    for page_num in page_numbers:
        try:
            content = parser.extract_page_content(page_num)
            extracted_pages.append(content)
            print(f"✅ Extracted page {page_num}")
        except ValueError as e:
            print(f"⚠️  Skipping page {page_num}: {e}")
    
    return extracted_pages


def extract_page_range(
    parser: 'AutomotiveDatasheetParser',
    start_page: int,
    end_page: int,
    filter_register_only: bool = True,
    filter_tables_only: bool = True
) -> List[Dict]:
    """
    Extract content from a page range with optional filtering
    
    Args:
        parser: Instance of AutomotiveDatasheetParser
        start_page: Starting page number (0-indexed, inclusive)
        end_page: Ending page number (0-indexed, inclusive)
        filter_register_only: Only return pages with register content
        filter_tables_only: Only return pages with tables
        
    Returns:
        List of page content dictionaries
        
    Example:
        # Extract pages 50-100 with registers and tables
        pages = extract_page_range(parser, 50, 100)
        
        # Extract all pages 10-20 regardless of content
        pages = extract_page_range(parser, 10, 20, 
                                   filter_register_only=False,
                                   filter_tables_only=False)
    """
    if start_page < 0:
        raise ValueError("start_page must be >= 0")
    
    if end_page >= parser.metadata['page_count']:
        print(f"⚠️  end_page {end_page} exceeds document length, "
              f"setting to {parser.metadata['page_count'] - 1}")
        end_page = parser.metadata['page_count'] - 1
    
    if start_page > end_page:
        raise ValueError(f"start_page ({start_page}) must be <= end_page ({end_page})")
    
    print(f"\n📄 Extracting pages {start_page} to {end_page}...")
    print(f"   Filters: register_only={filter_register_only}, "
          f"tables_only={filter_tables_only}")
    
    extracted_pages = []
    
    for page_num in range(start_page, end_page + 1):
        content = parser.extract_page_content(page_num)
        
        # Apply filters
        if filter_register_only and not content['is_register_page']:
            continue
        
        if filter_tables_only and content['table_count'] == 0:
            continue
        
        extracted_pages.append(content)
        print(f"  ✅ Page {page_num}: {content['table_count']} tables")
    
    print(f"✅ Extracted {len(extracted_pages)} pages from range")
    return extracted_pages


def find_register_table_pages(
    parser: 'AutomotiveDatasheetParser',
    start_page: int = 0,
    end_page: Optional[int] = None,
    min_tables: int = 1,
    keywords: Optional[List[str]] = None
) -> List[int]:
    """
    Find page numbers containing register tables within a range
    
    Args:
        parser: Instance of AutomotiveDatasheetParser
        start_page: Starting page (0-indexed)
        end_page: Ending page (0-indexed), None = last page
        min_tables: Minimum number of tables required
        keywords: Additional keywords to search for (optional)
        
    Returns:
        List of page numbers containing register tables
        
    Example:
        # Find all register pages in document
        pages = find_register_table_pages(parser)
        
        # Find register pages in specific range with custom keywords
        pages = find_register_table_pages(parser, 50, 150, 
                                         keywords=['I2C', 'SPI'])
    """
    if end_page is None:
        end_page = parser.metadata['page_count'] - 1
    
    if keywords is None:
        keywords = []
    
    print(f"\n🔍 Searching for register tables in pages {start_page}-{end_page}...")
    
    register_page_numbers = []
    
    for page_num in range(start_page, end_page + 1):
        content = parser.extract_page_content(page_num)
        
        # Check basic criteria
        if not content['is_register_page']:
            continue
        
        if content['table_count'] < min_tables:
            continue
        
        # Check for additional keywords if provided
        if keywords:
            text_lower = content['text'].lower()
            if not any(kw.lower() in text_lower for kw in keywords):
                continue
        
        register_page_numbers.append(page_num)
        print(f"  📋 Page {page_num}: {content['table_count']} tables found")
    
    print(f"✅ Found {len(register_page_numbers)} pages with register tables")
    return register_page_numbers


def extract_and_analyze_range(
    pdf_path: str,
    start_page: int,
    end_page: int,
    llm_model: str = "phi3:latest",
    output_dir: str = "output"
) -> Dict:
    """
    Complete pipeline: Extract page range -> Analyze with LLM -> Generate tests
    
    Args:
        pdf_path: Path to PDF datasheet
        start_page: Starting page (0-indexed)
        end_page: Ending page (0-indexed)
        llm_model: Ollama model to use
        output_dir: Output directory for results
        
    Returns:
        Dictionary with analysis results and file paths
        
    Example:
        # Process pages 80-120 and generate tests
        results = extract_and_analyze_range(
            "datasheets/stm32-f446re-RM.pdf",
            start_page=80,
            end_page=120
        )
    """
    from datasheet_parser.pdf_extractor import AutomotiveDatasheetParser
    from llm_service.ollama_client import AutomotiveTestLLM
    
    print(f"\n{'='*70}")
    print(f"🚀 RANGE-BASED ANALYSIS PIPELINE")
    print(f"{'='*70}\n")
    print(f"📄 PDF: {pdf_path}")
    print(f"📑 Page Range: {start_page} - {end_page}")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Step 1: Extract pages
    with AutomotiveDatasheetParser(pdf_path) as parser:
        pages = extract_page_range(
            parser,
            start_page,
            end_page,
            filter_register_only=True,
            filter_tables_only=True
        )
    
    if not pages:
        print("❌ No register tables found in specified range")
        return {"status": "error", "message": "No tables found"}
    
    # Step 2: Analyze with LLM
    print(f"\n🤖 Analyzing {len(pages)} pages with LLM ({llm_model})...")
    llm = AutomotiveTestLLM(model=llm_model)
    
    all_analyses = []
    robot_tests = []
    
    for page in pages:
        page_num = page['page_number']
        
        for table_idx, table in enumerate(page.get('tables', [])):
            print(f"  📊 Page {page_num}, Table {table_idx + 1}: "
                  f"{table['row_count']}×{table['column_count']}")
            
            # Analyze
            analysis = llm.analyze_register_table(table)
            
            if analysis['status'] == 'success':
                all_analyses.append({
                    'page': page_num,
                    'table': table_idx,
                    'analysis': analysis['analysis']
                })
                
                # Generate Robot test
                robot_test = llm.generate_robot_framework_test(analysis)
                robot_tests.append({
                    'page': page_num,
                    'table': table_idx,
                    'test_code': robot_test
                })
                print(f"     ✅ Analysis & test generation complete")
            else:
                print(f"     ❌ Failed: {analysis.get('error', 'Unknown')}")
    
    # Step 3: Save results
    print(f"\n💾 Saving results to {output_dir}/...")
    
    # Save analyses
    analyses_file = output_path / f"analyses_p{start_page}-{end_page}.json"
    with open(analyses_file, 'w') as f:
        json.dump({
            'pdf': str(pdf_path),
            'page_range': {'start': start_page, 'end': end_page},
            'pages_processed': len(pages),
            'tables_analyzed': len(all_analyses),
            'analyses': all_analyses
        }, f, indent=2)
    
    # Save Robot tests
    robot_file = output_path / f"tests_p{start_page}-{end_page}.robot"
    with open(robot_file, 'w') as f:
        f.write("*** Settings ***\n")
        f.write(f"Documentation    Auto-generated from pages {start_page}-{end_page}\n")
        f.write("Library          RegisterLibrary\n\n")
        
        for test in robot_tests:
            f.write(f"# Page {test['page']}, Table {test['table']}\n")
            f.write(test['test_code'])
            f.write("\n\n")
    
    print(f"  ✅ Analyses: {analyses_file}")
    print(f"  ✅ Robot tests: {robot_file}")
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 SUMMARY")
    print(f"{'='*70}")
    print(f"  Pages with tables: {len(pages)}")
    print(f"  Tables analyzed: {len(all_analyses)}")
    print(f"  Tests generated: {len(robot_tests)}")
    
    return {
        'status': 'success',
        'pages_processed': len(pages),
        'analyses_count': len(all_analyses),
        'tests_count': len(robot_tests),
        'output_files': {
            'analyses': str(analyses_file),
            'robot_tests': str(robot_file)
        }
    }


def interactive_page_selector(parser: 'AutomotiveDatasheetParser') -> Tuple[int, int]:
    """
    Interactive CLI for selecting page range
    
    Args:
        parser: Instance of AutomotiveDatasheetParser
        
    Returns:
        Tuple of (start_page, end_page)
        
    Example:
        with AutomotiveDatasheetParser("datasheet.pdf") as parser:
            start, end = interactive_page_selector(parser)
            pages = extract_page_range(parser, start, end)
    """
    print(f"\n📄 Document: {parser.metadata['filename']}")
    print(f"📖 Total pages: {parser.metadata['page_count']}")
    
    # Show sample of register pages
    print("\n🔍 Scanning for register pages...")
    sample_pages = find_register_table_pages(parser, 0, min(50, parser.metadata['page_count'] - 1))
    
    if sample_pages:
        print(f"\nSample register pages (first 10): {sample_pages[:10]}")
    
    # Get user input
    while True:
        try:
            start = int(input(f"\nEnter start page (0-{parser.metadata['page_count']-1}): "))
            if 0 <= start < parser.metadata['page_count']:
                break
            print(f"⚠️  Must be between 0 and {parser.metadata['page_count']-1}")
        except ValueError:
            print("⚠️  Please enter a valid number")
    
    while True:
        try:
            end = int(input(f"Enter end page ({start}-{parser.metadata['page_count']-1}): "))
            if start <= end < parser.metadata['page_count']:
                break
            print(f"⚠️  Must be between {start} and {parser.metadata['page_count']-1}")
        except ValueError:
            print("⚠️  Please enter a valid number")
    
    return start, end
