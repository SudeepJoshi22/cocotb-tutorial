TOPLEVEL_LANG ?= verilog

PWD=$(shell pwd)

export PYTHONPATH := $(PWD)/../model:$(PYTHONPATH)

VERILOG_SOURCES = $(PWD)/../hdl/alu.v

TOPLEVEL := alu
MODULE   := test_alu

include $(shell cocotb-config --makefiles)/Makefile.sim
