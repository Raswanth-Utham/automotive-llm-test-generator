"""
Ollama LLM Service for Automotive Test Generation
Connects to local Ollama instance and generates test cases from register data
"""

import json
import re
from typing import Dict, List, Optional
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

class AutomotiveTestLLM:
    """
    LLM service specialized for automotive register test case generation
    Uses local Ollama with optimized prompts for embedded systems
    """
    
    def __init__(
        self, 
        model: str = "phi3:latest",
        base_url: str = "http://127.0.0.1:11434",
        temperature: float = 0.3
    ):
        """
        Initialize Ollama LLM client
        
        Args:
            model: Ollama model name (default: llama3.2:3b)
            base_url: Ollama API endpoint
            temperature: Lower = more deterministic (0.3 good for test generation)
        """
        self.model = model
        self.base_url = base_url
        
        # Initialize Ollama LLM
        self.llm = OllamaLLM(
            model=model,
            base_url=base_url,
            temperature=temperature,
            format="json"
        )
        
        print(f"✅ Connected to Ollama: {model} at {base_url}")
    
    def analyze_register_table(self, table_data: Dict) -> Dict:
        """
        Analyze a register table and extract key test points
        
        Args:
            table_data: Dictionary containing table headers and rows
            
        Returns:
            Structured analysis with test scenarios
        """
        
        # Create prompt for register analysis
        prompt_template = PromptTemplate(
            input_variables=["headers", "rows", "table_context"],
            template="""You are an expert embedded systems test engineer specializing in automotive MCU testing.

Analyze this register table and identify test scenarios:

**Table Headers:** {headers}

**Table Rows (first 5 shown):**
{rows}

**Context:** {table_context}

Your task:
1. Identify the register name, address/offset, bit fields
2. Determine read/write permissions (RO, WO, RW)
3. Note reset/default values
4. Identify reserved or unused bits
5. Generate 3-5 critical test scenarios for this register

Output format (JSON):
{{
  "register_name": "extracted register name",
  "address": "register address or offset",
  "access_type": "RW/RO/WO",
  "reset_value": "default value",
  "test_scenarios": [
    "Test scenario 1 description",
    "Test scenario 2 description",
    "Test scenario 3 description"
  ],
  "boundary_conditions": ["condition 1", "condition 2"],
  "notes": "Any special considerations"
}}

Only output valid JSON, no additional text."""
        )
        
        # Prepare data
        headers_str = ", ".join(str(h) for h in table_data.get("headers", []))
        rows_data = table_data.get("rows", [])[:5]  # Limit to first 5 rows
        rows_str = "\n".join([str(row) for row in rows_data])
        
        # Detect context from headers
        context = self._detect_table_context(table_data)
        
        # Create chain
        chain = prompt_template | self.llm
        
        # Run analysis
        try:
            result = chain.invoke({
                "headers": headers_str,
                "rows": rows_str,
                "table_context": context
            })
            
            # Parse JSON response
            analysis = self._parse_llm_response(result)
            
            return {
                "status": "success",
                "analysis": analysis,
                "raw_response": result
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "analysis": None
            }
    
    def generate_robot_framework_test(self, register_analysis: Dict) -> str:
        """
        Generate Robot Framework test case from register analysis
        
        Args:
            register_analysis: Output from analyze_register_table()
            
        Returns:
            Robot Framework test case as string
        """
        
        if not register_analysis.get("analysis"):
            return "# Error: No analysis data available"
        
        analysis = register_analysis["analysis"]
        
        prompt_template = PromptTemplate(
            input_variables=["register_name", "address", "access_type", 
                           "reset_value", "test_scenarios"],
            template="""You are a Robot Framework test automation expert for embedded automotive systems.

Generate a Robot Framework test case for this register:

**Register:** {register_name}
**Address:** {address}
**Access Type:** {access_type}
**Reset Value:** {reset_value}

**Test Scenarios:**
{test_scenarios}

Create a well-structured Robot Framework test with:
- Test case name
- Documentation
- Setup and teardown keywords
- Test steps using keywords like: Read Register, Write Register, Verify Register Value, Reset Device
- Clear assertions

Output ONLY the Robot Framework test code, no explanations.

Example format:
*** Test Cases ***
Test {register_name} Default Value
    [Documentation]    Verify reset value of {register_name}
    [Tags]    registers    reset_values
    Reset Device
    ${{value}}=    Read Register    {address}
    Should Be Equal    ${{value}}    {reset_value}
"""
        )
        
        # Prepare test scenarios as string
        scenarios_str = "\n".join([f"- {s}" for s in analysis.get("test_scenarios", [])])
        
        chain = prompt_template | self.llm
        
        try:
            result = chain.invoke({
                "register_name": analysis.get("register_name", "Unknown"),
                "address": analysis.get("address", "0x00"),
                "access_type": analysis.get("access_type", "RW"),
                "reset_value": analysis.get("reset_value", "0x00"),
                "test_scenarios": scenarios_str
            })
            
            return result
            
        except Exception as e:
            return f"# Error generating Robot Framework test: {str(e)}"
    
    def _detect_table_context(self, table_data: Dict) -> str:
        """Detect what type of table this is based on headers"""
        headers = [str(h).lower() for h in table_data.get("headers", [])]
        
        if any(word in " ".join(headers) for word in ["register", "address", "offset"]):
            return "This appears to be a register map table"
        elif any(word in " ".join(headers) for word in ["bit", "field"]):
            return "This appears to be a bit field definition table"
        elif any(word in " ".join(headers) for word in ["timing", "delay"]):
            return "This appears to be a timing specification table"
        else:
            return "This is a technical specification table"
        
    def _parse_llm_response(self, response: str) -> Dict:
        """
        Parse LLM JSON response, handling potential formatting issues
        """
        import re
        try:
            text = (response or "").strip()

            # Prefer a fenced ```json ... ```
            m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text)
            if m:
                text = m.group(1)
            else:
                # Fallback: isolate the first { ... } object in the text
                start = text.find("{")
                end = text.rfind("}")
                if start != -1 and end != -1 and end > start:
                    text = text[start:end + 1]

            # Final parse
            return json.loads(text)

        except Exception as e:
            return {
                "register_name": "Parse Error",
                "error": f"Could not parse LLM JSON response: {e}",
                "raw_text": response,
            }

    
    def batch_analyze_registers(self, register_pages: List[Dict]) -> List[Dict]:
        """
        Analyze multiple register pages in batch
        
        Args:
            register_pages: List of page dictionaries with tables
            
        Returns:
            List of analysis results
        """
        results = []
        
        for page in register_pages:
            page_num = page.get("page_number", "unknown")
            print(f"\n📄 Analyzing page {page_num}...")
            
            for table_idx, table in enumerate(page.get("tables", [])):
                print(f"  📊 Table {table_idx + 1}/{len(page['tables'])}")
                
                analysis = self.analyze_register_table(table)
                
                results.append({
                    "page_number": page_num,
                    "table_index": table_idx,
                    "analysis": analysis
                })
        
        return results


# Convenience function for quick testing
def quick_test_llm():
    """Quick test of Ollama connectivity"""
    try:
        llm = AutomotiveTestLLM()
        
        # Test with simple prompt
        test_prompt = "You are a test engineer. Say 'Ollama is working!' in 5 words or less."
        response = llm.llm.invoke(test_prompt)
        
        print(f"\n✅ LLM Test Response: {response}")
        return True
    
    except Exception as e:
        print(f"\n❌ LLM Connection Failed: {e}")
        return False
