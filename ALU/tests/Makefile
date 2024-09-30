all:
	TOPLEVEL_LANG ?= verilog
	PWD=$(shell pwd)

	VERILOG_SOURCES = $(shell pwd)/../hdl/alu.sv

	MODULE = test_alu
	TOPLEVEL = alu

	include $(shell cocotb-config --makefiles)/Makefile.sim
clean:
	rm -rf sim_build/

.PHONY: all
