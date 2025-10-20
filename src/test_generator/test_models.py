"""
Pydantic models for representing logical test cases.
These structures are framework-agnostic and represent the "intent" of a test.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field

# Define types of tests for automotive validation
TestType = Literal[
            "reset_value",
                "read_write",
                    "boundary_value",
                        "invalid_write",
                            "state_transition",
                                "error_injection",
                                    "timing_check"
                                    ]

# Define ISO 26262 ASIL levels for safety requirement mapping
ASIL_Level = Literal["A", "B", "C", "D", "QM"]


class LogicalTestCase(BaseModel):
        """A framework-agnostic representation of a single test case."""
            
                name: str = Field(..., description="A descriptive name for the test case.")
                    description: str = Field(..., description="A detailed description of the test's purpose.")
                        test_type: TestType = Field(..., description="The category of the test.")
                            
                                # Parameters for the test execution
                                    register_name: str
                                        register_address: Optional[str] = None
                                            write_value: Optional[str] = None
                                                expected_value: Optional[str] = None
                                                    
                                                        # Metadata
                                                            tags: List[str] = Field(default_factory=list, description="Tags for filtering (e.g., 'gpio', 'spi').")
                                                                iso_26262_asil: Optional[ASIL_Level] = Field(None, description="Associated ASIL level for safety coverage.")
                                                                    
                                                                        class Config:
                                                                                    use_enum_values = True


                                                                                    class TestSuite(BaseModel):
                                                                                            """A collection of logical test cases for a specific component or register."""
                                                                                                
                                                                                                    suite_name: str
                                                                                                        source_file: str
                                                                                                            source_page: int
                                                                                                                test_cases: List[LogicalTestCase]
