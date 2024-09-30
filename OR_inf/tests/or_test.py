import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly, NextTimeStep
from cocotb_bus.driver import BusDriver

def cb_fn(actual_value):
    global expected_value
    assert actual_value == expected_value, f"Scoreboard Matching Failed"

@cocotb.test()
async def ifc_test(dut):
    a = (0,0,1,1)
    b = (0,1,0,1)
    #y = (0,1,1,1)
   
    expected_value = (0,1,1,1)
    
    dut.RST_N.value = 1
    await.Timer(1,'ns')
    dut.RST_N.value = 0
    await Timer(1,'ns')
    await RisingEdge(dut.CLK)
    dut.RST_N.value = 1

    adrv = InputDriver(dut,'a',dut.CLK)
    bdrv = InputDriver(dut,'b',dut.CLK)
    OutputDriver(dut,'y',dut.CLK, cb_fn) # Pass call-back function

    for i in range(4):
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
        if self.bus.rdy.value != 0:
            await RisingEdge(self.bus.rdy)
        self.en.value = 1
        self.bus.data.value = value

        await ReadOnly() # checking values from different always block might cause an error. So wait till the end of delta-delay cycle
        await RisingEdge(self.clk)
        await NextTimeStep()
        self.bus.en.value = 0

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
            if self.bus.rdy.value != 0:
                await RisingEdge(self.bus.rdy)
            self.en.value = 1
            #self.bus.data = value
            self.callback(self.bus.data.value) # Whatever data is obtained, pass it out of the function
            await ReadOnly() # checking values from different always block might cause an error. So wait till the end of delta-delay cycle
            await RisingEdge(self.clk)
            self.bus.en = 0
            await NextTimeStep()
