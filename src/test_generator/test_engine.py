"""
Test Engine for generating logical test cases from LLM analysis.
This module applies automotive testing principles to the suggestions from the LLM.
"""

from typing import Dict, List, Optional
from .test_models import LogicalTestCase, TestSuite, ASIL_Level

class TestCaseGenerator:
    """
    Generates a suite of logical test cases from the structured analysis
    provided by the LLM service.
    """
    
    def __init__(self, analysis_data: Dict, source_file: str, source_page: int):
        """
        Initialize the generator with analysis data.
        
        Args:
            analysis_data: The JSON output from the LLM's analysis.
            source_file: The name of the source PDF.
            source_page: The page number in the PDF where the data was found.
        """
        self.analysis = analysis_data.get("analysis", {})
        self.source_file = source_file
        self.source_page = source_page
        
        self.register_name = self.analysis.get("register_name", "UnknownRegister")
        self.address = self.analysis.get("address", "0x0000")
        self.access = self.analysis.get("access_type", "RW")
        self.reset_value = self.analysis.get("reset_value")

    def generate_suite(self) -> TestSuite:
        """
        Generate a full suite of test cases based on the analysis.
        """
        test_cases: List[LogicalTestCase] = []
        
        # 1. Generate Reset Value Test
        if self.reset_value and self.reset_value.lower() not in ["none", "unknown"]:
            test_cases.append(self._create_reset_value_test())
            
        # 2. Generate Read/Write Tests (if applicable)
        if "w" in self.access.lower():
            test_cases.extend(self._create_read_write_tests())
        
        # 3. Generate Boundary Tests
        # This is a placeholder; a real implementation would need bitfield info
        if self.analysis.get("boundary_conditions"):
            test_cases.extend(self._create_boundary_tests())
            
        suite = TestSuite(
            suite_name=f"Tests for {self.register_name}",
            source_file=self.source_file,
            source_page=self.source_page,
            test_cases=test_cases
        )
        
        return suite

    def _create_reset_value_test(self) -> LogicalTestCase:
        """Create a test to verify the register's reset value."""
        return LogicalTestCase(
            name=f"Verify Reset Value of {self.register_name}",
            description=f"Checks that the {self.register_name} register at address {self.address} defaults to its specified reset value of {self.reset_value} after a power-on reset.",
            test_type="reset_value",
            register_name=self.register_name,
            register_address=self.address,
            expected_value=self.reset_value,
            tags=[self.register_name.lower(), "reset", "power_on"],
            iso_26262_asil="B"  # Default ASIL for core register integrity
        )

    def _create_read_write_tests(self) -> List[LogicalTestCase]:
        """Create basic read/write tests."""
        tests = []
        
        # Test writing and reading a common pattern
        write_value = "0x55555555" # Example pattern
        tests.append(LogicalTestCase(
            name=f"Write/Read Test for {self.register_name}",
            description=f"Writes a pattern ({write_value}) to {self.register_name} and verifies it can be read back correctly.",
            test_type="read_write",
            register_name=self.register_name,
            register_address=self.address,
            write_value=write_value,
            expected_value=write_value,
            tags=[self.register_name.lower(), "read_write"],
            iso_26262_asil="B"
        ))
        
        # Test writing another pattern
        write_value_2 = "0xAAAAAAAA"
        tests.append(LogicalTestCase(
            name=f"Alternate Pattern Write/Read Test for {self.register_name}",
            description=f"Writes an alternate pattern ({write_value_2}) to ensure bits are not stuck.",
            test_type="read_write",
            register_name=self.register_name,
            register_address=self.address,
            write_value=write_value_2,
            expected_value=write_value_2,
            tags=[self.register_name.lower(), "read_write", "stuck_at"],
            iso_26262_asil="B"
        ))
        
        return tests
        
    def _create_boundary_tests(self) -> List[LogicalTestCase]:
        """Create tests based on LLM-suggested boundary conditions."""
        tests = []
        conditions = self.analysis.get("boundary_conditions", [])
        
        for i, condition in enumerate(conditions):
            tests.append(LogicalTestCase(
                name=f"Boundary Test {i+1} for {self.register_name}",
                description=f"Boundary condition test based on LLM suggestion: '{condition}'",
                test_type="boundary_value",
                register_name=self.register_name,
                register_address=self.address,
                tags=[self.register_name.lower(), "boundary"],
                # ASIL level might be higher for safety-critical boundaries
                iso_26262_asil="C" 
            ))
        
        return tests
