# Tcl learning helpers — run lesson examples with make
#
# Usage (from project root):
#   make help                 Show this help
#   make week1                Run all Week 1 examples in order
#   make week1-01             Run one Week 1 example (01..12)
#   make run WEEK=1 EX=10     Run lessons/1/10_*.tcl
#   make list WEEK=1          List Week 1 .tcl files
#   make check                Verify tclsh is available

ROOT      := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
LESSONS   := $(ROOT)lessons
TCLSH     ?= tclsh
WEEK      ?= 1
EX        ?= 01

.DEFAULT_GOAL := help

.PHONY: help check list run week1 week1-01 week1-02 week1-03 week1-04 \
	week1-05 week1-06 week1-07 week1-08 week1-09 week1-10 week1-11 week1-12

help:
	@echo "Tcl lesson runner"
	@echo ""
	@echo "  make week1           Run all Week 1 examples"
	@echo "  make week1-01        Run one example (01..12)"
	@echo "  make run WEEK=1 EX=10"
	@echo "  make list WEEK=1"
	@echo "  make check"
	@echo ""
	@echo "Examples:"
	@echo "  make week1-01"
	@echo "  make week1-10"
	@echo "  make run WEEK=1 EX=07"

check:
	@command -v $(TCLSH) >/dev/null 2>&1 || { \
		echo "error: $(TCLSH) not found. Install Tcl first."; exit 1; }
	@printf '%s\n' 'puts "tclsh OK (Tcl $$tcl_version)"' | $(TCLSH)

list:
	@echo "Week $(WEEK) scripts in lessons/$(WEEK)/"
	@ls -1 "$(LESSONS)/$(WEEK)/"*.tcl 2>/dev/null || \
		{ echo "error: no .tcl files in lessons/$(WEEK)/"; exit 1; }

# Run one example: make run WEEK=1 EX=10
run: check
	@file=$$(ls -1 "$(LESSONS)/$(WEEK)/$(EX)"*.tcl 2>/dev/null | head -n1); \
	if [ -z "$$file" ]; then \
		echo "error: no match for lessons/$(WEEK)/$(EX)*.tcl"; \
		echo "try: make list WEEK=$(WEEK)"; \
		exit 1; \
	fi; \
	echo "==> $$file"; \
	$(TCLSH) "$$file"

# Run every .tcl in a week folder, sorted
define RUN_WEEK
	@week_dir="$(LESSONS)/$(1)"; \
	if [ ! -d "$$week_dir" ]; then \
		echo "error: missing $$week_dir"; exit 1; \
	fi; \
	echo "=== Week $(1) — all examples ==="; \
	for f in $$(ls -1 "$$week_dir"/*.tcl | sort); do \
		echo ""; \
		echo "==> $$f"; \
		$(TCLSH) "$$f" || exit 1; \
	done; \
	echo ""; \
	echo "=== Week $(1) done ==="
endef

week1: check
	$(call RUN_WEEK,1)

week1-01: ; @$(MAKE) --no-print-directory run WEEK=1 EX=01
week1-02: ; @$(MAKE) --no-print-directory run WEEK=1 EX=02
week1-03: ; @$(MAKE) --no-print-directory run WEEK=1 EX=03
week1-04: ; @$(MAKE) --no-print-directory run WEEK=1 EX=04
week1-05: ; @$(MAKE) --no-print-directory run WEEK=1 EX=05
week1-06: ; @$(MAKE) --no-print-directory run WEEK=1 EX=06
week1-07: ; @$(MAKE) --no-print-directory run WEEK=1 EX=07
week1-08: ; @$(MAKE) --no-print-directory run WEEK=1 EX=08
week1-09: ; @$(MAKE) --no-print-directory run WEEK=1 EX=09
week1-10: ; @$(MAKE) --no-print-directory run WEEK=1 EX=10
week1-11: ; @$(MAKE) --no-print-directory run WEEK=1 EX=11
week1-12: ; @$(MAKE) --no-print-directory run WEEK=1 EX=12
