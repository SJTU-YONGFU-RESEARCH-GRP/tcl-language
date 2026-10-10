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

.PHONY: help check list run \
	week1 week1-01 week1-02 week1-03 week1-04 week1-05 week1-06 \
	week1-07 week1-08 week1-09 week1-10 week1-11 week1-12 \
	week2 week2-01 week2-02 week2-03 week2-04 week2-05 week2-06 \
	week2-07 week2-08 week2-09 week2-10 week2-11 week2-12 \
	week3 week3-01 week3-02 week3-03 week3-04 week3-05 week3-06 \
	week3-07 week3-08 week3-09 week3-10 week3-11 week3-12 \
	week4 week4-01 week4-02 week4-03 week4-04 week4-05 week4-06 \
	week4-07 week4-08 week4-09 week4-10 week4-11 week4-12 \
	week5 week5-01 week5-02 week5-03 week5-04 week5-05 week5-06 \
	week5-07 week5-08 week5-09 week5-10 week5-11 week5-12 \
	week6 week6-01 week6-02 week6-03 week6-04 week6-05 week6-06 \
	week6-07 week6-08 week6-09 week6-10 week6-11 week6-12

help:
	@echo "Tcl lesson runner"
	@echo ""
	@echo "  make week1           Run all Week 1 examples"
	@echo "  make week2           Run all Week 2 examples"
	@echo "  make week3           Run all Week 3 examples"
	@echo "  make week4           Run all Week 4 examples"
	@echo "  make week5           Run all Week 5 examples"
	@echo "  make week6           Run all Week 6 examples"
	@echo "  make week1-01        Run one Week 1 example (01..12)"
	@echo "  make week2-01        Run one Week 2 example (01..12)"
	@echo "  make week3-01        Run one Week 3 example (01..12)"
	@echo "  make week4-01        Run one Week 4 example (01..12)"
	@echo "  make week5-01        Run one Week 5 example (01..12)"
	@echo "  make week6-01        Run one Week 6 example (01..12)"
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

week2: check
	$(call RUN_WEEK,2)

week2-01: ; @$(MAKE) --no-print-directory run WEEK=2 EX=01
week2-02: ; @$(MAKE) --no-print-directory run WEEK=2 EX=02
week2-03: ; @$(MAKE) --no-print-directory run WEEK=2 EX=03
week2-04: ; @$(MAKE) --no-print-directory run WEEK=2 EX=04
week2-05: ; @$(MAKE) --no-print-directory run WEEK=2 EX=05
week2-06: ; @$(MAKE) --no-print-directory run WEEK=2 EX=06
week2-07: ; @$(MAKE) --no-print-directory run WEEK=2 EX=07
week2-08: ; @$(MAKE) --no-print-directory run WEEK=2 EX=08
week2-09: ; @$(MAKE) --no-print-directory run WEEK=2 EX=09
week2-10: ; @$(MAKE) --no-print-directory run WEEK=2 EX=10
week2-11: ; @$(MAKE) --no-print-directory run WEEK=2 EX=11
week2-12: ; @$(MAKE) --no-print-directory run WEEK=2 EX=12

week3: check
	$(call RUN_WEEK,3)

week3-01: ; @$(MAKE) --no-print-directory run WEEK=3 EX=01
week3-02: ; @$(MAKE) --no-print-directory run WEEK=3 EX=02
week3-03: ; @$(MAKE) --no-print-directory run WEEK=3 EX=03
week3-04: ; @$(MAKE) --no-print-directory run WEEK=3 EX=04
week3-05: ; @$(MAKE) --no-print-directory run WEEK=3 EX=05
week3-06: ; @$(MAKE) --no-print-directory run WEEK=3 EX=06
week3-07: ; @$(MAKE) --no-print-directory run WEEK=3 EX=07
week3-08: ; @$(MAKE) --no-print-directory run WEEK=3 EX=08
week3-09: ; @$(MAKE) --no-print-directory run WEEK=3 EX=09
week3-10: ; @$(MAKE) --no-print-directory run WEEK=3 EX=10
week3-11: ; @$(MAKE) --no-print-directory run WEEK=3 EX=11
week3-12: ; @$(MAKE) --no-print-directory run WEEK=3 EX=12

week4: check
	$(call RUN_WEEK,4)

week4-01: ; @$(MAKE) --no-print-directory run WEEK=4 EX=01
week4-02: ; @$(MAKE) --no-print-directory run WEEK=4 EX=02
week4-03: ; @$(MAKE) --no-print-directory run WEEK=4 EX=03
week4-04: ; @$(MAKE) --no-print-directory run WEEK=4 EX=04
week4-05: ; @$(MAKE) --no-print-directory run WEEK=4 EX=05
week4-06: ; @$(MAKE) --no-print-directory run WEEK=4 EX=06
week4-07: ; @$(MAKE) --no-print-directory run WEEK=4 EX=07
week4-08: ; @$(MAKE) --no-print-directory run WEEK=4 EX=08
week4-09: ; @$(MAKE) --no-print-directory run WEEK=4 EX=09
week4-10: ; @$(MAKE) --no-print-directory run WEEK=4 EX=10
week4-11: ; @$(MAKE) --no-print-directory run WEEK=4 EX=11
week4-12: ; @$(MAKE) --no-print-directory run WEEK=4 EX=12

week5: check
	$(call RUN_WEEK,5)

week5-01: ; @$(MAKE) --no-print-directory run WEEK=5 EX=01
week5-02: ; @$(MAKE) --no-print-directory run WEEK=5 EX=02
week5-03: ; @$(MAKE) --no-print-directory run WEEK=5 EX=03
week5-04: ; @$(MAKE) --no-print-directory run WEEK=5 EX=04
week5-05: ; @$(MAKE) --no-print-directory run WEEK=5 EX=05
week5-06: ; @$(MAKE) --no-print-directory run WEEK=5 EX=06
week5-07: ; @$(MAKE) --no-print-directory run WEEK=5 EX=07
week5-08: ; @$(MAKE) --no-print-directory run WEEK=5 EX=08
week5-09: ; @$(MAKE) --no-print-directory run WEEK=5 EX=09
week5-10: ; @$(MAKE) --no-print-directory run WEEK=5 EX=10
week5-11: ; @$(MAKE) --no-print-directory run WEEK=5 EX=11
week5-12: ; @$(MAKE) --no-print-directory run WEEK=5 EX=12

week6: check
	$(call RUN_WEEK,6)

week6-01: ; @$(MAKE) --no-print-directory run WEEK=6 EX=01
week6-02: ; @$(MAKE) --no-print-directory run WEEK=6 EX=02
week6-03: ; @$(MAKE) --no-print-directory run WEEK=6 EX=03
week6-04: ; @$(MAKE) --no-print-directory run WEEK=6 EX=04
week6-05: ; @$(MAKE) --no-print-directory run WEEK=6 EX=05
week6-06: ; @$(MAKE) --no-print-directory run WEEK=6 EX=06
week6-07: ; @$(MAKE) --no-print-directory run WEEK=6 EX=07
week6-08: ; @$(MAKE) --no-print-directory run WEEK=6 EX=08
week6-09: ; @$(MAKE) --no-print-directory run WEEK=6 EX=09
week6-10: ; @$(MAKE) --no-print-directory run WEEK=6 EX=10
week6-11: ; @$(MAKE) --no-print-directory run WEEK=6 EX=11
week6-12: ; @$(MAKE) --no-print-directory run WEEK=6 EX=12
