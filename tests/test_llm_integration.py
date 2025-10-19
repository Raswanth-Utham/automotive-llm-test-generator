"""
Test LLM integration with PDF parser
End-to-end test: PDF -> Tables -> LLM Analysis -> Robot Framework
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from datasheet_parser.pdf_extractor import AutomotiveDatasheetParser
from datasheet_parser.pdf_extractor_utilities import *
from llm_service.ollama_client import AutomotiveTestLLM, quick_test_llm


def test_full_pipeline(pdf_path: str, max_pages: int = 3):
    """
    Test complete pipeline: PDF -> Parse -> LLM -> Robot Framework
    
    Args:
        pdf_path: Path to datasheet PDF
        max_pages: Limit pages to analyze (for testing)
    """
    
    print(f"\n{'='*70}")
    print(f"🚀 FULL PIPELINE TEST: LLM-Powered Automotive Test Generator")
    print(f"{'='*70}\n")
    
    # Step 1: Test Ollama connectivity
    print("STEP 1: Testing Ollama Connection...")
    if not quick_test_llm():
        print("❌ Ollama connection failed. Is Ollama running?")
        print("   Run: sudo systemctl status ollama")
        return
    
    # Step 2: Parse PDF
    print("\nSTEP 2: Parsing Datasheet PDF...")
    with AutomotiveDatasheetParser(pdf_path) as parser:
        print(f"  📄 Document: {parser.metadata['filename']}")
        print(f"  📖 Pages: {parser.metadata['page_count']}")
        
        # Extract register pages
        register_pages = parser.extract_register_pages()
        print(f"  🔍 Found {len(register_pages)} pages with registers")
        
        if not register_pages:
            print("  ⚠️  No register pages detected. Using first page with tables.")
            # Fallback: get first page with tables
            for i in range(min(10, parser.metadata['page_count'])):
                page = parser.extract_page_content(i)
                if page['table_count'] > 0:
                    register_pages = [page]
                    break
        
        # Limit for testing
        register_pages = register_pages[:max_pages]
    
    if not register_pages:
        print("❌ No tables found in PDF. Cannot proceed.")
        return
    
    # Step 3: Analyze with LLM
    print(f"\nSTEP 3: Analyzing {len(register_pages)} pages with LLM...")
    llm = AutomotiveTestLLM()
    
    all_analyses = []
    robot_tests = []
    
    for page in register_pages:
        page_num = page['page_number']
        tables = page.get('tables', [])
        
        print(f"\n  📄 Page {page_num}: {len(tables)} tables")
        
        for table_idx, table in enumerate(tables[:2]):  # Max 2 tables per page for demo
            print(f"    📊 Analyzing Table {table_idx + 1}...")
            print(f"       Dimensions: {table['row_count']} rows × {table['column_count']} cols")
            
            # Analyze table
            analysis = llm.analyze_register_table(table)
            
            if analysis['status'] == 'success':
                print(f"       ✅ Analysis complete")
                
                # Store analysis
                all_analyses.append({
                    'page': page_num,
                    'table': table_idx,
                    'analysis': analysis['analysis']
                })
                
                # Generate Robot Framework test
                print(f"       🤖 Generating Robot Framework test...")
                robot_test = llm.generate_robot_framework_test(analysis)
                robot_tests.append({
                    'page': page_num,
                    'table': table_idx,
                    'test_code': robot_test
                })
                print(f"       ✅ Robot test generated")
            
            else:
                print(f"       ❌ Analysis failed: {analysis.get('error', 'Unknown error')}")
    
    # Step 4: Save results
    print("\n" + "="*70)
    print("STEP 4: Saving Results...")
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Save analyses as JSON
    analyses_file = output_dir / "llm_analyses.json"
    with open(analyses_file, 'w') as f:
        json.dump(all_analyses, f, indent=2)
    print(f"  💾 Analyses saved: {analyses_file}")
    
    # Save Robot Framework tests
    robot_file = output_dir / "generated_tests.robot"
    with open(robot_file, 'w') as f:
        f.write("*** Settings ***\n")
        f.write("Documentation    Auto-generated tests from STM32 datasheet\n")
        f.write("Library          RegisterLibrary\n\n")
        
        for test in robot_tests:
            f.write(f"# Page {test['page']}, Table {test['table']}\n")
            f.write(test['test_code'])
            f.write("\n\n")
    
    print(f"  🤖 Robot Framework tests saved: {robot_file}")
    
    # Step 5: Summary
    print("\n" + "="*70)
    print("📊 PIPELINE SUMMARY")
    print("="*70)
    print(f"  Pages analyzed: {len(register_pages)}")
    print(f"  Tables processed: {sum(len(p.get('tables', [])) for p in register_pages)}")
    print(f"  Successful analyses: {len(all_analyses)}")
    print(f"  Robot tests generated: {len(robot_tests)}")
    
    # Show sample analysis
    if all_analyses:
        print("\n📋 SAMPLE ANALYSIS:")
        sample = all_analyses[0]['analysis']
        print(json.dumps(sample, indent=2))
    
    # Show sample Robot test
    if robot_tests:
        print("\n🤖 SAMPLE ROBOT FRAMEWORK TEST:")
        print(robot_tests[0]['test_code'][:500] + "...")
    
    print("\n✅ Pipeline test complete!")
    print(f"\n📁 Check output/ folder for full results")

def test_page_range_analysis(pdf_path: str, start_page: int, end_page: int):
    """
    Test pipeline with specific page range
    
    Usage:
        python test_llm_integration.py <pdf> --range 80 120
    """
    results = extract_and_analyze_range(
        pdf_path=pdf_path,
        start_page=start_page,
        end_page=end_page,
        llm_model="phi3:latest"
    )
    
    if results['status'] == 'success':
        print("\n✅ Range analysis complete!")
        print(f"📁 Check {results['output_files']['robot_tests']} for tests")
    else:
        print(f"\n❌ Analysis failed: {results.get('message', 'Unknown error')}")


def test_find_register_pages(pdf_path: str):
    """
    Test function to find all register table page numbers
    
    Usage:
        python test_llm_integration.py <pdf> --find-pages
    """
    print(f"\n{'='*70}")
    print(f"🔍 FINDING REGISTER TABLE PAGES")
    print(f"{'='*70}\n")
    
    with AutomotiveDatasheetParser(pdf_path) as parser:
        # Find all register pages
        all_pages = find_register_table_pages(parser)
        
        print(f"\n📋 Register Table Pages Found: {len(all_pages)}")
        print(f"\nPage numbers: {all_pages[:50]}")  # Show first 50
        
        if len(all_pages) > 50:
            print(f"... and {len(all_pages) - 50} more pages")
        
        # Save to file
        output_file = Path("output/register_pages.json")
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump({
                'pdf': str(pdf_path),
                'total_pages': parser.metadata['page_count'],
                'register_pages_count': len(all_pages),
                'register_pages': all_pages
            }, f, indent=2)
        
        print(f"\n💾 Saved page numbers to: {output_file}")


# Update main to handle new arguments
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python test_llm_integration.py <pdf> [max_pages]")
        print("  python test_llm_integration.py <pdf> --range <start> <end>")
        print("  python test_llm_integration.py <pdf> --find-pages")
        print("\nExamples:")
        print("  python test_llm_integration.py datasheet.pdf 3")
        print("  python test_llm_integration.py datasheet.pdf --range 80 120")
        print("  python test_llm_integration.py datasheet.pdf --find-pages")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if len(sys.argv) > 2 and sys.argv[2] == "--range":
        # Range mode
        start = int(sys.argv[3])
        end = int(sys.argv[4])
        test_page_range_analysis(pdf_path, start, end)
    
    elif len(sys.argv) > 2 and sys.argv[2] == "--find-pages":
        # Find pages mode
        test_find_register_pages(pdf_path)
    
    else:
        # Original mode
        max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        test_full_pipeline(pdf_path, max_pages)
