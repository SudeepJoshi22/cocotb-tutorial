import cocotb
import random
from cocotb.triggers import Timer, RisingEdge, ReadOnly, NextTimeStep
from cocotb_bus.drivers import BusDriver

def cb_fn(actual_value):
    global expected_value
    assert actual_value == expected_value.pop(0), f"Scoreboard Matching Failed"

@cocotb.test()
async def ifc_test(dut):
    a = (0,0,1,1)
    b = (0,1,0,1)
    #y = (0,1,1,1)
    
    global expected_value
    expected_value = [] 
    
    dut.RST_N.value = 1
    await Timer(1,'ns')
    dut.RST_N.value = 0
    await Timer(1,'ns')
    await RisingEdge(dut.CLK)
    dut.RST_N.value = 1

    adrv = InputDriver(dut,'a',dut.CLK)
    bdrv = InputDriver(dut,'b',dut.CLK)
    OutputDriver(dut,'y',dut.CLK, cb_fn) # Pass call-back function

    for i in range(4):
        print(f"a:{a[i]}")
        print(f"b:{b[i]}")
        print(f"y:{a[i] | b[i]}")
        expected_value.append(a[i] | b[i])
        print(f"Expected list: {expected_value}")
        #print(f"Expected list: {expected_value.pop(0)}")
        adrv.append(a[i])
        bdrv.append(b[i])

    while len(expected_value) > 0:
        await(Timer(2,'ns'))

class InputDriver(BusDriver):
    _signals = ['en', 'rdy', 'data']

    def __init__(self, dut, name, clk):
        BusDriver.__init__(self, dut, name, clk)
        self.bus.en.value = 0
        self.clk = clk
    async def _driver_send(self, value, sync = True):
        for i in range(random.randint(0, 20)):
            await RisingEdge(self.clk)
        
        if self.bus.rdy.value != 1:
            await RisingEdge(self.bus.rdy)
        self.bus.en.value = 1
        self.bus.data.value = value

        await ReadOnly() # checking values from different always block might cause an error. So wait till the end of delta-delay cycle
        await RisingEdge(self.clk)
        self.bus.en.value = 0
        await NextTimeStep()

class OutputDriver(BusDriver):
    _signals = ['en', 'rdy', 'data']

    def __init__(self, dut, name, clk, sb_callback):
        BusDriver.__init__(self, dut, name, clk)
        self.bus.en.value = 0
        self.clk = clk
        self.callback = sb_callback
        self.append(0)

    async def _driver_send(self, value, sync = True):
        while True:
            if self.bus.rdy.value != 1:
                await RisingEdge(self.bus.rdy)
            self.bus.en.value = 1
            #self.bus.data = value
            await ReadOnly() # checking values from different always block might cause an error. So wait till the end of delta-delay cycle
            self.callback(self.bus.data.value) # Whatever data is obtained, pass it out of the function
            await RisingEdge(self.clk)
            await NextTimeStep()
            self.bus.en.value = 0
