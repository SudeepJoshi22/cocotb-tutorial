import os
import random
import sys
from pathlib import Path

import cocotb
from cocotb.runner import get_runner
from cocotb.triggers import Timer

if cocotb.simulator.is_running():
    from alu_model import alu_model


BIT_WIDTH = 32

alu_operations = [
    "add",    # 0b000
    "sub",    # 0b001
    "and",    # 0b010
    "or",     # 0b011
    "xor",    # 0b100
    "gt",     # 0b101 (Greater Than, signed)
    "gtu",    # 0b110 (Greater Than, unsigned)
    "eq"      # 0b111 (Equal)
]

@cocotb.test()
async def alu_basic_test(dut):
    """Basic Directed Test"""

    A = 10
    B = -20
    
    dut.A.value = A
    dut.B.value = B
    
    for ALU_Sel in range(8): 
        dut.ALU_Sel.value = ALU_Sel

        await Timer(2, units="ns")

        expected_value = alu_model(A, B, alu_operations[ALU_Sel], BIT_WIDTH)
        
        assert dut.ALU_Result.value == expected_value, f"ALU result is incorrect: {dut.ALU_Result.value} != {expected_value}"
	

@cocotb.test()
async def alu_randomised_test(dut):
    """Test for adding 2 random numbers multiple times"""

    for i in range(10):

        A = random.randint(-3200, 3200)
        B = random.randint(-3200, 3200)
        ALU_Sel = random.randint(0,7) 
        
        dut.A.value = A
        dut.B.value = B
        dut.ALU_Sel.value = ALU_Sel

        await Timer(2, units="ns")

        expected_value = alu_model(A, B, alu_operations[ALU_Sel], BIT_WIDTH)
        
        assert dut.ALU_Result.value == expected_value, f"ALU result is incorrect: {dut.ALU_Result.value} != {expected_value}"

def test_alu_runner():
    """Simulate the ALU example using the Python runner.

    This file can be run directly or via pytest discovery.
    """

    sim = os.getenv("SIM", "icarus")

    proj_path = Path(__file__).resolve().parent.parent
    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "model"))

    verilog_sources = []

    verilog_sources = [proj_path / "hdl" / "alu.v"]

    build_test_args = []

    # equivalent to setting the PYTHONPATH environment variable
    sys.path.append(str(proj_path / "tests"))

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        vhdl_sources=vhdl_sources,
        hdl_toplevel="alu",
        always=True,
        build_args=build_test_args,
    )
    runner.test(
        hdl_toplevel="alu", test_module="test_alu", test_args=build_test_args
    )


if __name__ == "__main__":
    test_alu_runner()
