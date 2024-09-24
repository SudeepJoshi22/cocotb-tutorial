# Test Design in Cocotb - simple example to get started
import cocotb

from cocotb.triggers import Timer


# Also clock can be generated using Helper function like this
async def generate_clock(dut):
    """Generate clock pulses."""

    for cycle in range(10):
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")
        
'''
- To call the helper clock generator
await cocotb.start(generate_clock(dut))  # run the clock "in the background"

await Timer(5, units="ns")  # wait a bit
await FallingEdge(dut.clk)  # wait for falling edge/"negedge"

Since generating a clock is such a common task, cocotb provides a helper for it - cocotb.clock.Clock. No need to write your own clock generator!

You would start Clock with cocotb.start_soon(Clock(dut.clk, 1, units="ns").start()) near the top of your test, after importing it with from cocotb.clock import Clock.
'''

@cocotb.test()
async def my_design_test(dut):
	""" Accessing the Design """
	for cycles in range(30):
		dut.clk.value = 0
	        await Timer(1, units="ns")
		dut.clk.value = 1
		await Timer(1, units="ns")
	dut._log.info("My signal1 is %s", dut.my_signal1.value)
	assert dut.my_signal2.value[0] == 0, "my_signal2[0] is not 0!"
