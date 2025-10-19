*** Settings ***
Documentation    Auto-generated from pages 186-190
Library          RegisterLibrary

# Page 186, Table 0
{
    "Test Cases": {
        "Verify OSPEEDR8 writes and reads correctly with valid speed values": {
            "#1: Default Value":"",
            "#2: Write/Read Valid Speed Values Test Scenario": ""
        },
        "Test boundary conditions for max and min allowed speeds in OSPEEDR8 to ensure proper saturation handling": {
            "#1: Boundary Conditions Test Scenario Description": "",
            "#2:":"",
            "#3: Validate Max Speed Saturation":"",
            "#4: Validate Min Speed Saturation":""
        },
        "Simulate write-while-read scenario on OSPEEDR8 to verify data integrity during concurrent access": {
            "#1: Write/Read Concurrent Access Test Scenario Description": "",
            "#2:":"",
            "#3: Simulate Writing Speed Value":"",
            "#4: Simulate Reading Speed Value":"",
            "#5: Verify Data Integrity During Concurrency":""
        }
    },
    "Keywords": {
        "Reset Device": "Given device is powered on and ready to test OSPEEDR8 register, When I reset the device, Then it should be in a known state with default values for all registers",
        "Read Register": "When reading from memory at address ${address} (decimal), And interpreting data as binary string of length {length}, Then I should get value ${expected_value}",
        "Write Register": "When writing to the OSPEEDR8 register with speed value ${speed_value}, And ensuring access type is RW, Then it should be written successfully",
        "Verify Register Value": "And then verify that reading from memory at address 31-24 (decimal) returns exactly {expected_register_value}",
        "Should Be Equal": "{actual value} and [None, None, 'rw', ... ] should be equal"
    }
}

# Page 186, Table 1
{
    "Test Setup": {
        "Given":"Device is powered on and OSPEEDR7 register is accessible",
        "When":"OSPEEDR7 value has been set correctly using Write Register command with extreme values for testing edge cases",
        "Then":"All conditions are met, including data integrity during concurrent operations if applicable"
    },
    "Test Case 1: Verify Writing and Reading OSPEEDR7 Value": {
        "Setup":{},
        "Test Steps":[
            "* Log in to the embedded system",
            "Write Register [OSPEEDR7] with a specific non-extreme value, e.g., '0x5A' (using Robot Framework keywords like WriteRegister)",
            "Read OSPEEDR7 register and capture its current state"
        ],
        "Teardown":{},
        "Assertions":[
            "* Verify that the written value is equal to expected non-extreme value, e.g., 'Should Be Equal 0x5A ${read_value}' (using Robot Framework keywords like Should Be Equal)"
        ]
    },
    "Test Case 2: Test Boundary Conditions for OSPEEDR7": {
        "Setup":{},
        "Test Steps":[
            "* Log in to the embedded system",
            "Write Register [OSPEEDR7] with extreme values, e.g., '0xFF' and then again after resetting using Reset Device keyword"
        ],
        "Teardown":{},
        "Assertions":[
            "* Verify that the initial write of all ones is equal to expected value 0xFF",
            "* After device reset, verify OSPEEDR7 reads back 'None specified; assuming default to rw' (using Robot Framework keywords like Read Register and Should Be Equal)"
        ]
    },
    "Test Case 3: Concurrent Operations on OSPEEDR7": {
        "Setup":{},
        "Test Steps":[
            "* Log in to the embedded system",
            "Write a specific value, e.g., '0x5A' (using WriteRegister keyword)",
            "Simultaneously initiate another write operation with different values"
        ],
        "Teardown":{},
        "Assertions":[
            "* Verify that the final read of OSPEEDR7 register value is consistent and correct, e.g., 'Should Be Equal 0x5A ${final_read_value}' (using Read Register keyword)"
        ]
    }
}

# Page 186, Table 2
{
    "# Test PUPDR9[1:0] Default Value":"Verify reset value of PUPDR9[1:0]"
    }

# Page 186, Table 3
{
    "Test Cases": [
        {
            "Name": "Verify PUPDR7[1:0] default value",
            "Documentation": "Verify reset value of PUPDR7[1:0] is as expected.",
            "Setup": [],
            "Teardown": [],
            "Test Steps": [
                {
                    "Name": "Reset Device",
                    "Keywords": ["Reset Device"]
                },
                {
                    "Name": "Read PUPDR7[1:0] after reset",
                    "Keywords": ["Read Register"],
                    "Arguments": [{"Offset": 4, "Address": "${PUPDR7_ADDRESS}"}]
                },
                {
                    "Name": "Should Be Equal PUPDR7[1:0] to reset value",
                    "Keywords": ["Should Be Equal"],
                    "Arguments": [{"Actual Value": "${value}", "Expected Value": "${PUPDR7_RESET_VALUE}"}]
                }
            ],
            "Assertions": []
        },
        {
            "Name": "Write and Read PUPDR7[1:0] with valid data",
            "Documentation": "Writing to PUPDR7[1:0] should set the register correctly, which can then be read back.",
            "Setup": [],
            "Teardown": [],
            "Test Steps": [
                {
                    "Name": "Write 0x05 to PUPDR7[1:0]",
                    "Keywords": ["Write Register"],
                    "Arguments": [{"Offset": 4, "Address": "${PUPDR7_ADDRESS}", "Data Value": "0x05"}]
                },
                {
                    "Name": "Read PUPDR7[1:0] after write",
                    "Keywords": ["Read Register"],
                    "Arguments": [{"Offset": 4, "Address": "${PUPDR7_ADDRESS}"}]
                },
                {
                    "Name": "Should Be Equal PUPDR7[1:0] to written value",
                    "Keywords": ["Should Be Equal"],
                    "Arguments": [{"Actual Value": "${value}", "Expected Value": "0x05"}]
                }
            ],
            "Assertions": []
        },
        {
            "Name": "Write and Read PUPDR7[1:0] with extreme binary states",
            "Documentation": "Testing the register's behavior when set to all ones or all zeros.",
            "Setup": [],
            "Teardown": [],
            "Test Steps": [
                {
                    "Name": "Write 0xFF to PUPDR7[1:0]",
                    "Keywords": ["Write Register"],
                    "Arguments": [{"Offset": 4, "Address": "${PUPDR7_ADDRESS}", "Data Value": "0xFF"}]
                },
                {
                    "Name": "Read PUPDR7[1:0] after write",
                    "Keywords": ["Read Register"],
                    "Arguments": [{"Offset": 4, "Address": "${PUPDR7_ADDRESS}"}]
                },
                {
                    "Name": "Should Be Equal PUPDR7[1:0] to written value",
                    "Keywords": ["Should Be Equal"],
                    "Arguments": [{"Actual Value": "${value}", "Expected Value": "0xFF"}]
                }
            ],
            "Assertions": []
        },
        {
            "Name": "Simulate rapid read-write sequence on PUPDR7[1:0]",
            "Documentation": "Testing the register's response time under high frequency access patterns.",
            "Setup": [],
            "Teardown": [],
            "Test Steps": [
                {
                    "Name": "Write 0x02 to PUPDR7[1:0]",
                    "Keywords": ["Write Register"],
                    "Arguments": [{"Offset": 4, "Address": "${PUPDR7_ADDRESS}", "Data Value": "0x02"}]
                },
                {
                    "Name": "Read PUPDR7[1:0] after write",
                    "Keywords": ["Read Register"],
                    "Arguments": [{"Offset": 4, "Address": "${PUPDR7_ADDRESS}"}]
                }
            ],
            "Assertions": []
        }
    ]
}

# Page 187, Table 0
{
    "# Test Case: Control Register A (CRA) Default Value":"Verify CRA initializes to the reset value when power is applied.",
    "* Keywords *":["Setup", "Reset Device", "Test Step: Read Initial State of CR A", "Test Step: Verify Reset Value"],
    "*** Test Steps ***":[],
    "*** Keywords ***":{},
    "*** Teardown ***":[]
}

# Page 187, Table 1
{
    "Test Cases": {
        "Verify IDR15 can be read and written to": {
            "Documentation": "Ensure the register IDR15 is readable and writable.",
            "Setup": [],
            "Teardown": [],
            "Test Steps": [
                "- Open connection with embedded automotive system",
                "- Reset Device to initialize registers"
            ],
            "Assertions": []
        },
        "Write and read non-'r' value for IDR15, verify data integrity": {
            "Documentation": "Test writing a specific value other than 'r' into the register IDR15 and reading it back to ensure no corruption.",
            "Setup": [],
            "Teardown": [
                "- Close connection with embedded automotive system"
            ],
            "Test Steps": [
                "- Open connection",
                "- Write Register    Offset: 0xF (Table Header)    Value: 'a'",
                "- Read Register    Offset: 0xF (Table Header)",
                "- Should Be Equal    2nd value from register to expected non-'r' character"
            ],
            "Assertions": [
                {"name": "Should be equal", "msg_id": "", "type": "equality", "expected": "'a'"}
            ]
        },
        "Concurrent access handling for IDR15 register": {
            "Documentation": "Ensure proper synchronization when multiple threads/processes attempt to write and read the register simultaneously.",
            "Setup": [],
            "Teardown": [
                "- Close connection with embedded automotive system"
            ],
            "Test Steps": [
                "- Open connection",
                "- Start concurrent test thread 1: Write Register    Offset: 0xF (Table Header)    Value: 'b' and Read Register at the same time",
                "- Start concurrent test thread 2: Write Register    Offset: 0xF (Table Header)    Value: 'c' and Read Register at the same time"
            ],
            "Assertions": [
                {"name": "Should be equal", "msg_id": "", "type": "equality", "expected": "'b'}"},
                {"name": "Should be equal", "msg_id": "", "type": "equality", "expected": "'c'}"}
            ]
        }
    },
    "Keywords": {
        "Open Connection": "GUILibrary.open_connection",
        "Reset Device": "DeviceCommunication.reset_device"
    }
}

# Page 187, Table 2
{
    "test_name": "Test PCR Write and Read Operations",
    "docstring": "This test case verifies the ability of writing new duty cycle values and reading them back correctly from PWM Control Register.",
    "setup": "* Set up steps before running tests, if any (e.g., initializing hardware or software environment)",
    "teardown": "* Cleanup actions after tests run",
    "test_cases": [
        {
            "name": "Write and Read PCR Duty Cycle Value Test",
            "docstring": "Verify that the PWM Control Register (PCR) can be written with a new duty cycle value, which is then read back correctly.",
            "test_steps": [
                "* Initial setup steps if necessary"
                ],
                "assertions": [
                    {
                        "name": "Verify PCR Writes and Reads Duty Cycle Value",
                        "description": "Write a new duty cycle value to the PWM Control Register (PCR) and verify it is read back correctly.",
                        "steps": [
                            "* Write operation steps"
                            ],
                            "assertions": [
                                {
                                    "name": "Verify Written Duty Cycle Value",
                                    "description": "Check if the written duty cycle value is correctly reflected in PCR.",
                                    "steps": [
                                        "* Read operation steps"
                                        ],
                                        "assertions": [
                                            {
                                                "name": "Verify Correct Duty Cycle Value",
                   ",  ":"Should Be Equal","description":"The value read from PCR should match the written duty cycle.",
                    "value_to_compare": "${expected_duty_cycle}"
                            }
                        ]
                    }
                ],
                "* Teardown steps if necessary":"Cleanup actions after test",
                "":"Test Steps and Assertions for setting frequency of PWM using PCR to various values within operational limits, then reading it back for validation.",
            "assertions": [
                    {
                        "name": "Verify Written Frequency Value in PCR",
   ",  ":"Should Be Equal","description":"The value read from PCR should match the written frequency within operational limits."}
                ]
            }
        ],
         "* Write operation steps for setting and reading back various frequencies":"Read Register    0x3C\n...",
    "teardown": [
                  "* Teardown actions if necessary"
              ]
}
































# Page 187, Table 3
{
    "# Test ODR15 Write and Read Functionality":"Verify that writing to ODR15 sets the corresponding bit and clears all others.",
    "Documentation":"># This test case verifies if a write operation on register 'ODR15' correctly sets one specific bit while clearing other bits, ensuring proper functionality of output data registers in automotive systems. The expected behavior is that after writing to the ODR15 with an active signal (logic high), only this particular bit should be set and all others cleared.",
    "Setup":[],
    "Teardown":["Reset Device"],
    "Test Cases":{
        "# Test Case 0: Write Operation on Register ODR15":"Verify that writing to ODR15 sets the corresponding bit while clearing other bits."
        
        },
        "* Keywords *":[
            "# Read Current Value of Register ODR15", "Read Register", "- |- ${value}=    Get Reg Value   Offset: -16 (Decimal) or $FFD0h (Hexadecimal)"
            
            ],
            "# Write New Bit to Register ODR15":"Write a new bit value of 1 into register 'ODR15' and verify the change.",
            
            "* Keywords *":[
                "# Set Value on Register ODR15", "Set Reg Value","- |- ${value}=    Write To Reg   Offset: -16 (Decimal) or $FFD0h (Hexadecimal)", 
                
                "# Verify the Bit is set in Register after Writing","Verify Register Value","Should Contain      ${reg_name}     '${expected value}'", "- |- reg_name:    ODR15, expected value:  0x2 (Binary representation of bit being tested)"
                
            ]
            
        }

# Page 187, Table 4
{
    "Test Suite": {
        "Test Cases": [
            {
                "Name": "Write and Verify Non-Zero Value Across BR0 to BR15 Registers",
                "Documentation": "Writes a non-zero value across all BCM registers for the CAN Bus Module, then verifies correct storage.",
                "Setup": [],
                "Teardown": [],
                "Test Steps": [
                    {
                        "Name": "Write Non-Zero Value to BR0",
                        "Operation": "Write Register",
                        "Arguments": {"address": "32:0", "value": 1}
                    },
                    {
                        "Name": "Verify Written Value in BR0",
                        "Operation": "Read Register",
                        "Arguments": {"address": "32:0"}
                    },
                    {
                        "Name": "Write Non-Zero Values to Other BCM Registries (BR1 to BR15)",
                        "Operation": "Loop Operation with Write and Read Register",
                        "Arguments": [{"address_range": {"start": 32, "end": 48}, "value": 1}],
                        "Loop Arguments": {
                            "operation": ["Write Register", "Read Register"],
                            "arguments": [
                                {"address": "${address}", "value": 1}
                            ]
                        }
                    },
                    {
                        "Name": "Verify Written Values in All BCM Registries (BR0 to BR15)",
                        "Operation": "Read Register",
                        "Arguments": {"address_range": {"start": 32, "end": 48}}
                    }
                ],
                "Assertions": [
                    {
                        "Name": "All BCM Registries Contain Non-Zero Value"
                    }
                ]
            },
            {
                "Name": "Read Back Each Register After Writing Values",
                "Documentation": "Ensures data integrity by reading back each register after writing values.",
                "Setup": [],
                "Teardown": [],
                "Test Steps": [
                    {
                        "Name": "Write Non-Zero Value to BR0 and Read Back",
                        "Operation": "Read Register"
                    }
                ],
                "Assertions": [
                    {
                        "Name": "Written value in BR0 equals read back value for non-zero write operation."
                    }
                ]
            },
            {
 
                "Name": "Write Specific Value and Read Back Multiple Times",
                "Documentation": "Ensures reliability of write/read operations across all BCM registers by writing a specific value.",
                "Setup": [],
                "Teardown": [],
                "Test Steps": [
                    {
                        "Name": "Write Specific Value to BR0",
                        "Operation": "Write Register"
                    },
                    {
                        "Name": "Read Back Written Value in BR0 Multiple Times",
                        "Operation": "Loop Operation with Read Register",
                        "Arguments": [{"address": 32, "value": "<specific_value>"}],
                        "Loop Arguments": {"times": 5}
                    }
                ],
                "Assertions": [
                    {
                        "Name": "Written value in BR0 equals read back value for multiple reads."
                    }
                ]
            },
            {
                "Name": "Perform Boundary Testing on BCM Registers",
                "Documentation": "Verifies that no data corruption or overflow occurs at the maximum and minimum values allowed.",
                "Setup": [],
                "Teardown": [],
                "Test Steps": [
                    {
                        "Name": "Write Maximum Value to BR0",
                        "Operation": "Write Register"
                    },
                    {
                        "Name": "Read Back Written Maximum Value in BR0",
                        "Operation": "Read Register"
                    },
                    {
                        "Name": "Write Minimum Value to BR15 and Read Back Written Minimum Value in BR15",
                        "Operation": "Loop Operation with Write and Read Register",
                        "Arguments": [{"address_range": {"start": 48, "end": 64}, "value": "<minimum_value>"}],
                        "Loop Arguments": {
                            "operation": ["Write Register", "Read Register"],
                            "arguments": [
                                {"address": "${address}", "value": "<minimum_value>"}
                            ]
                        }
                    }
                ],
                "Assertions": [
                    {
                        "Name": "Written maximum value in BR0 equals read back written maximum value."
                    },
                    {
                        "Name": "Written minimum value in BR15 equals read back written minimum value."
                    }
                ]
            }
        ],
        "Keywords": [
            {"Read Register": "*"},
            {"Write Register": "*"}
        ]
    }
}

# Page 187, Table 5
{
    "# Test BS15 Default Value":"Verify reset value of BS15",
    "Documentation":"This test verifies that the default reset value for register BS15 is 'w'.",
    "Setup":[],
    "Teardown":[],
    "Test Steps":[
        "- Open device connection using [Setup Device] keyword.",
        "- Reset Device to ensure all registers start with their initial values using [Reset Device].",
        "- Read the value of register BS15 and store it in a variable ${value} by executing 'Read Register 0x008F'.",
        "Should Be Equal    ${value}    w"
    ],
    "Assertions":[],
    "Keywords":{
        "[Setup Device]":"Open device connection.",
        "[Reset Device]":"Perform hardware reset operation."
    }
}

# Page 188, Table 0
{
    "# Test Case for Writing and Reading the 'LCK K16' register with various data patterns":"Test Write-Read Cycle of LCK K16 Register",
    "*** Settings ***":[],
    "*** Test Cases ***":[{
        "# Verify that writing to a read/write field in 'LCK K16' and reading back works correctly.":["Verify RW Field Write-Read Correctness"],
        "# Check the write-read cycle with maximum values allowed by bit widths of fields within LCK K16 register, handling edge cases properly.":"Test Maximum Value Edge Case for 'LCK K16' Register",
        "# Ensure proper error checking when writing invalid data to a field that is marked as read/write but should be treated differently (e.g., non-zero value where it shouldn't).":"Test Invalid Write Data Handling in LCK K16 Readonly Fields"
    }],
    "*** Keywords ***":{
        "# Resets the device to its default state.":["Reset Device"],
        "# Writes a specific pattern of data into the 'LCK K16' register and returns the value written back by reading it from hardware or simulation environment.":"Write Register",
        "# Reads the current value stored in the specified address range (offset) within the device memory.":["Read Register"],
        "# Verifies that a specific expected value is equal to what was read from 'LCK K16' register after writing data into it and reading back.":"Verify Register Value"
    }
}

# Page 188, Table 1
{
    "Test Suite": "LCK Register Tests",
    "Version": "1.0",
    "Scenarios": {
        "K15 Default Value": {
            "Documentation": "Verify reset value of LCK K15 register after device reset.",
            "Setup": "",
            "Teardown": "",
            "Test Steps": [
                "- Goto Device Reset State",
                "${value}=    Read Register    Offset: 0x0F (Decimal: 15)",
                "Should Be Equal    ${value}    0"
            ],
            "Tags": ["registers", "reset_values"]
        },
        "K15 Write and Read Integrity": {
            "Documentation": "Verify that writing a specific pattern to LCK K15 register results in the expected behavior.",
            "Setup": "",
            "Teardown": "",
            "Test Steps": [
                "- Define test data with write value",
                "${write_value}=    Set Variable    '0xABCD' # Example pattern to be written, replace with actual values as needed.  ",
                "Write Register Offset: 0x0F (Decimal: 15) With Value=${write_value}",
                "- Read back the register value",
                "${read_value}=    Read Register    Offset: 0x0F (Decimal: 15)",
                "Should Be Equal    ${read_value}    0xABCD"
            ],
            "Tags": ["registers"]
        },
        "K15 Concurrent Access Test": {
            "Documentation": "Test concurrent read-write access patterns on LCK K15 register.",
            "Setup": "",
            "Teardown": "",
            "Test Steps": [
                "- Start a thread to write data",
                "${thread_code}=    Create String Variable    'Write Register Offset: 0x0F (Decimal: 15) With Value=SomeValue' # Replace with actual code for concurrent writing.",
                -1, "Start Thread Using Keyword    ${thread_code}",
                "- Start a thread to read data",
                "${read_thread_code}=    Create String Variable    'Read Register Offset: 0x0F (Decimal: 15)' # Replace with actual code for concurrent reading.",
                -2, "Start Thread Using Keyword    ${read_threads_code}",
                "- Join threads",
                "${join_threads_code}=    Create List Variable     '${threads}'"
            ],
            "Tags": ["registers"]
        },
        "K15 Power Failure Recovery Test": {
            "Documentation": "Simulate power failure scenarios where reads from LCK K15 return default values and verify system stability post recovery.",
            "Setup": "",
            "Teardown": "",
            "Test Steps": [
                "- Simulate Power Failure",
                "${simulated_power_failure_code}=    Create String Variable    'Simulate power failure' # Replace with actual code to simulate a power failure.",
                -1, "Start Keyword Using Code Execution    ${simulated_power_failure_code}",
                "- Read LCK K15 register after simulating power fail",
                "${read_value}=    Read Register Offset: 0x0F (Decimal: 15)",
                "Should Be Equal    ${read_value}    0"
            ],
            "Tags": ["registers"]
        }
    }
}

# Page 189, Table 0
{
    "Test Setup": {
        "Device Initialization": [
            "*Initial setup steps if needed*",
            ""
        ]
    },
    "Teardown": [
        "*Clean up after test, such as resetting the device or closing connections*"
    ],
    "Test Cases": {
        "Verify Default Value of AFRL7[3:0] Register After Reset": {
            "Documentation": "This tests that writing a specific pattern and then reading back yields the same value, testing write/read functionality.",
            "Setup": [
                "*Set up before test begins*",
                ""
            ],
            "Test Steps": [
                "Read Register AFRL7 starting at address offset +16 (assuming a base register before this)",
                "${value}=    Read Registry[AFRL7] Starting At Address Offset ${OFFSET}",
                "Should Be Equal 0x${SPECIFIC_PATTERN}    ${value}"
            ],
            "Teardown": [
                "*Tear down after test ends*",
                ""
            ]
        },
        "Verify High Bits in AFRL7[3:0] Register Returns Maximum Value": {
            "Documentation": "Test setting all bits to high, read operation should return maximum unsigned integer representable by this register size.",
            "Setup": [
                "*Set up before test begins*",
                ""
            ],
            "Test Steps": [
                "Write High Bits in AFRL7[3:0] Register",
                "${value}=    Write Registry[AFRL7] With Value 0x${MAX_UNSIGNED} (15)",
                "Read Back From AFRL7[3:0] Register",
                "${read_back}=    Read Registry[AFRL7] Starting At Address Offset ${OFFSET}",
                "Should Be Equal 0x${MAX_UNSIGNED}    ${read_back}"
            ],
            "Teardown": [
                "*Tear down after test ends*",
                ""
            ]
        },
        "Verify Write Integrity for AFRL7[3:0] Register with Zeros Followed by a 'Write' and Read Back Values": {
            "Documentation": "Ensures write integrity when writing zeros across all bit fields of AFRL7[3:0] followed by another 'write'.",
            "Setup": [
                "*Set up before test begins*",
                ""
            ],
            "Test Steps": [
                "Write Zeros Across All Bit Fields in AFRL7[3:0] Register",
                "${value}=    Write Registry[AFRL7] With Value 0x${ZERO_VALUE}",
                "Read Back From AFRL7[3:0] Register After First 'Zero' Operation",
                "${readback1}=    Read Registry[AFRL7] Starting At Address Offset ${OFFSET}",
                "Should Be Equal 0x${ZERO_VALUE}    ${readback1}"
            ],
            "Test Steps Continued": [
                "Write Another Value to AFRL7[3:0] Register",
                "${value2}=    Write Registry[AFRL7] With Value X (assuming a specific value)",
                "Read Back From AFRL7[3:0] Register After Second 'Write' Operation",
                "${readback2}=    Read Registry[AFRL7] Starting At Address Offset ${OFFSET}",
                "Should Be Equal 0x${VALUE_X}    ${readback2}"
            ],
            "Teardown": [
                "*Tear down after test ends*",
                ""
            ]
        },
        "Boundary Testing for Each Bit Field in AFRL7[3:0] Register": {
            "Documentation": "Perform boundary testing on each individual bit field to ensure correct behavior when setting bits high or low.",
            "Setup": [
                "*Set up before test begins*",
                ""
            ],
            "Test Steps": [
                "Write High Bit in AFRL7[3] Register and Read Back Value",
                "${value}=    Write Registry[AFRL7][0x4]= 1 (assuming bit-addressing for each field)",
                "${readback}=    Read Registry[AFRL7] Starting At Address Offset ${OFFSET}",
                "Should Be Equal 0b${HIGH_BIT} | (${LOW_BUTTONS})    0x${READBACK}"
            ],
            "Test Steps Continued": [
                "*Repeat for each bit field, setting high and low bits individually*",
                ""
            ],
            "Teardown": [
                "*Clean up after test ends*",
0.5 
        ]
    }
}
































# Page 189, Table 1
{
    "Test Suite": "AFRL3[3:0] Register Tests",
    "Scenarios": [
        {
            "Name": "Verify write operations set the correct values in AFRL3[3:0]",
            "Documentation": "This test case verifies that writing specific patterns to the AFRL3 register sets the expected bits.",
            "Setup": [],
            "Teardown": ["Reset Device"],
            "Test Steps": [
                {
                    "Name": "Write pattern 1",
                    "Keywords": ["Set Variable"]
                },
                {
                    "Name": "Verify write operation for AFRL3[0] and AFRL3[1] with bit patterns A, B respectively.",
                    "Keywords": [
                        "Write Register",
                        "AFRL3"
                    ],
                    "Arguments": {
                        "value": "${A}",
                        "offset_0": 0
                    }
                },
                {
                    "Name": "Verify write operation for AFRL3[2] with bit pattern C.",
                    "Keywords": [
                        "Write Register",
                        "AFRL3"
                    ],
                    "Arguments": {
                        "value": "${C}",
                        "offset_1": 0,
                        "bit_lengths": ["2"]
                    }
                },
                {
                    "Name": "Verify write operation for AFRL3[3] with bit pattern D.",
                    "Keywords": [
                        "Write Register",
                        "AFRL3"
                    ],
                    "Arguments": {
                        "value": "${D}",
                        "offset_2": 0,
                        "bit_lengths": ["1"]
                    }
                },
                {
                    "Name": "Verify write operations set the correct values in AFRL3[3:0]",
                    "Keywords": [
                        "Read Register"
                    ],
                    "Arguments": {
                        "address": "AFRL3",
                        "offsets": ["1", "2"]
                    },
                    "Expectation": "[Should Be Equal] ${B} AFRL3[0]"
                }
            ]
        },
        {
            "Name": "Confirm readback of written data from AFRL3[3:0] matches input value to ensure integrity after writing and reading cycles.",
            "Documentation": "This test case confirms that the values written into AFRL3 are correctly readable back out, ensuring write-read cycle integrity.",
            "Setup": [],
            "Teardown": ["Reset Device"],
            "Test Steps": [
                {
                    "Name": "Write pattern 2",
                    "Keywords": ["Set Variable"]
                },
                {
                    "Name": "Verify write operation for AFRL3[0] and AFRL3[1] with bit patterns E, F respectively.",
                    "Keywords": [
                        "Write Register",
                        "AFRL3"
                    ],
                    "Arguments": {
                        "value": "${E}",
                        "offset_0": 0
                    }
                },
                {
                   "Name": "Verify write operation for AFRL3[2] with bit pattern G.",
                   "Keywords": [
                       "Write Register",
                       "AFRL3"
                   ],
                   "Arguments": {
                       "value": "${G}",
                       "offset_1": 0,
                       "bit_lengths": ["2"]
                    }
                },
                {
                    "Name": "Verify write operation for AFRL3[3] with bit pattern H.",
                    "Keywords": [
                        "Write Register",
                        "AFRL3"
                    ],
                    "Arguments": {
                        "value": "${H}",
                        "offset_2": 0,
                        "bit_lengths": ["1"]
                    }
                },
                {
                   "Name": "Verify readback of written data from AFRL3[3:0] matches input value",
                   "Keywords": [
                       "Read Register"
                   ],
                   "Arguments": {
                        "address": "AFRL3",
                        "offsets": ["1", "2"]
                    },
                    "Expectation": "[Should Be Equal] ${F} AFRL3[0]"
                }
            ]
        },
        {
            "Name": "Test write-read cycle with boundary values for each bit field in AFRL3[3:0].",
            "Documentation": "This test case tests the register behavior at its boundaries, ensuring robustness of read and write operations.",
            "Setup": [],
            "Teardown": ["Reset Device"],
            "Test Steps": [
                {
                    "Name": "Write boundary values to AFRL3[0]",
                    "Keywords": ["Set Variable"]
                },
                {
                    "Name": "Verify write operation for AFRL3[0] with bit pattern 1.",
                    "Keywords": [
                        "Write Register",
                        "AFRL3"
                    ],
                    "Arguments": {
                        "value": "${B}",
                        "offset_0": 0,
                        "bit_lengths": ["1"]
                    }
                },
                {
                   "Name": "Verify readback of written data from AFRL3[0] matches input value",
                   "Keywords": [
                       "Read Register"
                   ],
                   "Arguments": {
                        "address": "AFRL3",
                        "offsets": ["1"]
                    },
                    "Expectation": "[Should Be Equal] ${B} AFRL3[0]"
                }
            ]
        }
    ],
    "Keywords": {
        "Set Variable": [
            "*",
            "Create Variable"
        ],
        "Read Register": ["*"],
        "Write Register": ["*"]
    }
}

