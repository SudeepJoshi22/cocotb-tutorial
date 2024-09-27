# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

TOPLEVEL_LANG ?= verilog
PWD=$(shell pwd)

VERILOG_SOURCES = $(shell pwd)/../hdl/FSM.sv

MODULE = test_FSM
TOPLEVEL = FSM

include $(shell cocotb-config --makefiles)/Makefile.sim
