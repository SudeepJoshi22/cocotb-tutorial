TOPLEVEL_LANG ?= verilog
PWD=$(shell pwd)

VERILOG_SOURCES = $(shell pwd)/../hdl/or_gate.v

MODULE = or_test
TOPLEVEL = or_gate

include $(shell cocotb-config --makefiles)/Makefile.sim

remove:
	rm -rf sim_build
