SHELL := /bin/bash

# Set variables
TOPLEVEL_LANG ?= verilog
PWD=$(shell pwd)
VERILOG_SOURCES = $(PWD)/../hdl/FSM.sv
MODULE = test_FSM
TOPLEVEL = FSM

# Include Cocotb Makefile for simulation (this will automatically handle the targets)
include $(shell cocotb-config --makefiles)/Makefile.sim

clean:
	rm -rf sim_build/

.PHONY: all clean
