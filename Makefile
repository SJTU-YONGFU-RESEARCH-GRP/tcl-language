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
CALIBRE   := $(ROOT)scripts/run_calibre_tcl.sh
CALIBRE_WEEK_MIN := 7
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
	week6-07 week6-08 week6-09 week6-10 week6-11 week6-12 \
	week7 week7-01 week7-02 week7-03 week7-04 week7-05 week7-06 \
	week7-07 week7-08 week7-09 week7-10 week7-11 week7-12 \
	week8 week8-01 week8-02 week8-03 week8-04 week8-05 week8-06 \
	week8-07 week8-08 week8-09 week8-10 week8-11 week8-12 \
	week9 week9-01 week9-02 week9-03 week9-04 week9-05 week9-06 \
	week9-07 week9-08 week9-09 week9-10 week9-11 week9-12 \
	week10 week10-01 week10-02 week10-03 week10-04 week10-05 week10-06 \
	week10-07 week10-08 week10-09 week10-10 week10-11 week10-12 \
	week11 week11-01 week11-02 week11-03 week11-04 week11-05 week11-06 \
	week11-07 week11-08 week11-09 week11-10 week11-11 week11-12 \
	check-calibre help-tcl help-calibre

help:
	@echo "Tcl lesson runner"
	@echo ""
	@echo "  make week1           Run all Week 1 examples"
	@echo "  make week2           Run all Week 2 examples"
	@echo "  make week3           Run all Week 3 examples"
	@echo "  make week4           Run all Week 4 examples"
	@echo "  make week5           Run all Week 5 examples"
	@echo "  make week6           Run all Week 6 examples"
	@echo "  make week7           Run all Week 7 examples (calibredrv)"
	@echo "  make week8           Run all Week 8 examples (calibredrv)"
	@echo "  make week9           Run all Week 9 examples (calibredrv)"
	@echo "  make week10          Run all Week 10 examples (calibredrv)"
	@echo "  make week11          Run all Week 11 examples (calibredrv, optional)"
	@echo "  make week1-01        Run one Week 1 example (01..12)"
	@echo "  make week2-01        Run one Week 2 example (01..12)"
	@echo "  make week3-01        Run one Week 3 example (01..12)"
	@echo "  make week4-01        Run one Week 4 example (01..12)"
	@echo "  make week5-01        Run one Week 5 example (01..12)"
	@echo "  make week6-01        Run one Week 6 example (01..12)"
	@echo "  make week7-01        Run one Week 7 example (01..12, calibredrv)"
	@echo "  make week8-01        Run one Week 8 example (01..12, calibredrv)"
	@echo "  make week9-01        Run one Week 9 example (01..12, calibredrv)"
	@echo "  make week10-01       Run one Week 10 example (01..12, calibredrv)"
	@echo "  make week11-01       Run one Week 11 example (01..12, calibredrv)"
	@echo "  make run WEEK=1 EX=10"
	@echo "  make list WEEK=1"
	@echo "  make check"
	@echo "  make help-tcl        Show Tcl discovery tips"
	@echo "  make help-calibre    Show Calibre Usage tips"
	@echo ""
	@echo "Examples:"
	@echo "  make week1-01"
	@echo "  make week1-10"
	@echo "  make run WEEK=1 EX=07"

check:
	@command -v $(TCLSH) >/dev/null 2>&1 || { \
		echo "error: $(TCLSH) not found. Install Tcl first."; exit 1; }
	@printf '%s\n' 'puts "tclsh OK (Tcl $$tcl_version)"' | $(TCLSH)

check-calibre:
	@test -x "$(CALIBRE)" || { \
		echo "error: $(CALIBRE) not found or not executable."; exit 1; }
	@$(CALIBRE) examples/hello_calibre.tcl >/dev/null
	@echo "calibredrv OK (via run_calibre_tcl.sh)"

help-tcl:
	@$(TCLSH) "$(ROOT)tools/show_tcl_help.tcl"

help-calibre: check-calibre
	@$(CALIBRE) "$(ROOT)tools/show_calibre_help.tcl"

list:
	@echo "Week $(WEEK) scripts in lessons/$(WEEK)/"
	@ls -1 "$(LESSONS)/$(WEEK)/"*.tcl 2>/dev/null || \
		{ echo "error: no .tcl files in lessons/$(WEEK)/"; exit 1; }

# Run one example: make run WEEK=1 EX=10
# Weeks 7+ use calibredrv via scripts/run_calibre_tcl.sh
run:
	@file=$$(ls -1 "$(LESSONS)/$(WEEK)/$(EX)"*.tcl 2>/dev/null | head -n1); \
	if [ -z "$$file" ]; then \
		echo "error: no match for lessons/$(WEEK)/$(EX)*.tcl"; \
		echo "try: make list WEEK=$(WEEK)"; \
		exit 1; \
	fi; \
	if [ "$(WEEK)" -ge $(CALIBRE_WEEK_MIN) ]; then \
		$(MAKE) --no-print-directory check-calibre; \
		echo "==> $$file (calibredrv)"; \
		$(CALIBRE) "$$file"; \
	else \
		$(MAKE) --no-print-directory check; \
		echo "==> $$file"; \
		$(TCLSH) "$$file"; \
	fi

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

define RUN_WEEK_CALIBRE
	@week_dir="$(LESSONS)/$(1)"; \
	if [ ! -d "$$week_dir" ]; then \
		echo "error: missing $$week_dir"; exit 1; \
	fi; \
	echo "=== Week $(1) — all examples (calibredrv) ==="; \
	for f in $$(ls -1 "$$week_dir"/*.tcl | sort); do \
		echo ""; \
		echo "==> $$f"; \
		$(CALIBRE) "$$f" || exit 1; \
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

week7: check-calibre
	$(call RUN_WEEK_CALIBRE,7)

week7-01: ; @$(MAKE) --no-print-directory run WEEK=7 EX=01
week7-02: ; @$(MAKE) --no-print-directory run WEEK=7 EX=02
week7-03: ; @$(MAKE) --no-print-directory run WEEK=7 EX=03
week7-04: ; @$(MAKE) --no-print-directory run WEEK=7 EX=04
week7-05: ; @$(MAKE) --no-print-directory run WEEK=7 EX=05
week7-06: ; @$(MAKE) --no-print-directory run WEEK=7 EX=06
week7-07: ; @$(MAKE) --no-print-directory run WEEK=7 EX=07
week7-08: ; @$(MAKE) --no-print-directory run WEEK=7 EX=08
week7-09: ; @$(MAKE) --no-print-directory run WEEK=7 EX=09
week7-10: ; @$(MAKE) --no-print-directory run WEEK=7 EX=10
week7-11: ; @$(MAKE) --no-print-directory run WEEK=7 EX=11
week7-12: ; @$(MAKE) --no-print-directory run WEEK=7 EX=12

week8: check-calibre
	$(call RUN_WEEK_CALIBRE,8)

week8-01: ; @$(MAKE) --no-print-directory run WEEK=8 EX=01
week8-02: ; @$(MAKE) --no-print-directory run WEEK=8 EX=02
week8-03: ; @$(MAKE) --no-print-directory run WEEK=8 EX=03
week8-04: ; @$(MAKE) --no-print-directory run WEEK=8 EX=04
week8-05: ; @$(MAKE) --no-print-directory run WEEK=8 EX=05
week8-06: ; @$(MAKE) --no-print-directory run WEEK=8 EX=06
week8-07: ; @$(MAKE) --no-print-directory run WEEK=8 EX=07
week8-08: ; @$(MAKE) --no-print-directory run WEEK=8 EX=08
week8-09: ; @$(MAKE) --no-print-directory run WEEK=8 EX=09
week8-10: ; @$(MAKE) --no-print-directory run WEEK=8 EX=10
week8-11: ; @$(MAKE) --no-print-directory run WEEK=8 EX=11
week8-12: ; @$(MAKE) --no-print-directory run WEEK=8 EX=12

week9: check-calibre
	$(call RUN_WEEK_CALIBRE,9)

week9-01: ; @$(MAKE) --no-print-directory run WEEK=9 EX=01
week9-02: ; @$(MAKE) --no-print-directory run WEEK=9 EX=02
week9-03: ; @$(MAKE) --no-print-directory run WEEK=9 EX=03
week9-04: ; @$(MAKE) --no-print-directory run WEEK=9 EX=04
week9-05: ; @$(MAKE) --no-print-directory run WEEK=9 EX=05
week9-06: ; @$(MAKE) --no-print-directory run WEEK=9 EX=06
week9-07: ; @$(MAKE) --no-print-directory run WEEK=9 EX=07
week9-08: ; @$(MAKE) --no-print-directory run WEEK=9 EX=08
week9-09: ; @$(MAKE) --no-print-directory run WEEK=9 EX=09
week9-10: ; @$(MAKE) --no-print-directory run WEEK=9 EX=10
week9-11: ; @$(MAKE) --no-print-directory run WEEK=9 EX=11
week9-12: ; @$(MAKE) --no-print-directory run WEEK=9 EX=12

week10: check-calibre
	$(call RUN_WEEK_CALIBRE,10)

week10-01: ; @$(MAKE) --no-print-directory run WEEK=10 EX=01
week10-02: ; @$(MAKE) --no-print-directory run WEEK=10 EX=02
week10-03: ; @$(MAKE) --no-print-directory run WEEK=10 EX=03
week10-04: ; @$(MAKE) --no-print-directory run WEEK=10 EX=04
week10-05: ; @$(MAKE) --no-print-directory run WEEK=10 EX=05
week10-06: ; @$(MAKE) --no-print-directory run WEEK=10 EX=06
week10-07: ; @$(MAKE) --no-print-directory run WEEK=10 EX=07
week10-08: ; @$(MAKE) --no-print-directory run WEEK=10 EX=08
week10-09: ; @$(MAKE) --no-print-directory run WEEK=10 EX=09
week10-10: ; @$(MAKE) --no-print-directory run WEEK=10 EX=10
week10-11: ; @$(MAKE) --no-print-directory run WEEK=10 EX=11
week10-12: ; @$(MAKE) --no-print-directory run WEEK=10 EX=12

week11: check-calibre
	$(call RUN_WEEK_CALIBRE,11)

week11-01: ; @$(MAKE) --no-print-directory run WEEK=11 EX=01
week11-02: ; @$(MAKE) --no-print-directory run WEEK=11 EX=02
week11-03: ; @$(MAKE) --no-print-directory run WEEK=11 EX=03
week11-04: ; @$(MAKE) --no-print-directory run WEEK=11 EX=04
week11-05: ; @$(MAKE) --no-print-directory run WEEK=11 EX=05
week11-06: ; @$(MAKE) --no-print-directory run WEEK=11 EX=06
week11-07: ; @$(MAKE) --no-print-directory run WEEK=11 EX=07
week11-08: ; @$(MAKE) --no-print-directory run WEEK=11 EX=08
week11-09: ; @$(MAKE) --no-print-directory run WEEK=11 EX=09
week11-10: ; @$(MAKE) --no-print-directory run WEEK=11 EX=10
week11-11: ; @$(MAKE) --no-print-directory run WEEK=11 EX=11
week11-12: ; @$(MAKE) --no-print-directory run WEEK=11 EX=12
