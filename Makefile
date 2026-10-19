# Tcl learning helpers — run lesson examples with make
#
# Usage (from project root):
#   make help                 Show this help
#   make week1                Run all Week 1 examples in order
#   make week1-01             Run one Week 1 example (01..12)
#   make run WEEK=1 EX=10     Run lessons/1/10_*.tcl
#   make list WEEK=1          List Week 1 .tcl files
#   make check                Verify tclsh is available
#
# Milestones: M10=1–10 Tcl syntax · M20=11–20 fluency+OOP · M30=21–30 Calibre · M40=31–40 catalog
# Runtime: weeks 1–20 → tclsh; weeks ≥21 → calibredrv

ROOT      := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
LESSONS   := $(ROOT)lessons
TCLSH     ?= tclsh
CALIBRE   := $(ROOT)scripts/run_calibre_tcl.sh
CALIBRE_WEEK_MIN := 21
WEEK      ?= 1
EX        ?= 01

# Weeks with lesson folders present today (others: generate via content-generation)
EXISTING_WEEKS := 1 2 3 4 5 6 15 21 22 23 24 25 26 27 28

.DEFAULT_GOAL := help

.PHONY: help check check-env check-calibre list run help-tcl help-calibre milestones \
	drvlite-test timing-demo \
	site site-serve site-install \
	week1 week2 week3 week4 week5 week6 week15 \
	week21 week22 week23 week24 week25 week26 week27 week28 \
	$(foreach w,1 2 3 4 5 6 15 21 22 23 24 25 26 27 28,$(foreach n,01 02 03 04 05 06 07 08 09 10 11 12,week$(w)-$(n)))

help:
	@echo "Tcl lesson runner (Tcl-first curriculum)"
	@echo ""
	@echo "  Milestones:  M10 weeks 1–10   Tcl syntax"
	@echo "               M20 weeks 11–20  fluency + OOP"
	@echo "               M30 weeks 21–30  Calibre core"
	@echo "               M40 weeks 31–40  Calibre catalog"
	@echo ""
	@echo "  make weekN           Run all examples in lessons/N/ (if present)"
	@echo "  make weekN-01        Run one example (01..12)"
	@echo "  make run WEEK=N EX=10"
	@echo "  make list WEEK=N"
	@echo "  make milestones      Print roadmap"
	@echo "  make check / check-calibre"
	@echo "  make help-tcl / help-calibre"
	@echo "  make site-install    Install MkDocs deps"
	@echo "  make site            Build lesson website → website/site/"
	@echo "  make site-serve      Local preview http://127.0.0.1:8000"
	@echo ""
	@echo "  Present folders: $(EXISTING_WEEKS)"
	@echo "  Runtime: weeks 1–20 = tclsh; weeks >=$(CALIBRE_WEEK_MIN) = calibredrv"
	@echo ""
	@echo "Examples:"
	@echo "  make week1-01"
	@echo "  make week6            # string toolkit (M10)"
	@echo "  make week15           # TclOO"
	@echo "  make week21-01        # first Calibre week"

milestones:
	@echo "M10  weeks 1–10   Tcl syntax core (puts … dict / errors)"
	@echo "M20  weeks 11–20  fluency + TclOO + pure-Tcl capstone"
	@echo "M30  weeks 21–30  Calibre core (layout … boolean + catalog start)"
	@echo "M40  weeks 31–40  Calibre encyclopedia + coverage audit"
	@echo "See PLAN.md and lessons/README.md"

check:
	@command -v $(TCLSH) >/dev/null 2>&1 || { \
		echo "error: $(TCLSH) not found. Install Tcl first."; exit 1; }
	@printf '%s\n' 'puts "tclsh OK (Tcl $$tcl_version)"' | $(TCLSH)

check-calibre:
	@test -x "$(CALIBRE)" || { \
		echo "error: $(CALIBRE) not found or not executable."; exit 1; }
	@$(CALIBRE) examples/hello_calibre.tcl >/dev/null
	@echo "calibredrv OK (via run_calibre_tcl.sh)"

check-env: check
	@echo "--- Environment Check ---"
	@command -v calibredrv >/dev/null 2>&1 && echo "Calibre DESIGNrev : INSTALLED (native hardware)" || echo "Calibre DESIGNrev : NOT FOUND (will use pure-Tcl DRV-Lite simulator)"
	@test -f "$(ROOT)tools/drvlite/drvlite.tcl" && echo "DRV-Lite Simulator: READY ($(ROOT)tools/drvlite/drvlite.tcl)" || echo "DRV-Lite Simulator: MISSING"

drvlite-test:
	@$(TCLSH) "$(ROOT)tools/drvlite/test_drvlite.tcl"

timing-demo:
	@$(TCLSH) "$(ROOT)examples/timing_report_analyzer.tcl"

help-tcl:
	@$(TCLSH) "$(ROOT)tools/show_tcl_help.tcl"

help-calibre: check-calibre
	@$(CALIBRE) "$(ROOT)tools/show_calibre_help.tcl"

list:
	@echo "Week $(WEEK) scripts in lessons/$(WEEK)/"
	@ls -1 "$(LESSONS)/$(WEEK)/"*.tcl 2>/dev/null || \
		{ echo "error: no .tcl files in lessons/$(WEEK)/ (not generated yet — see PLAN.md)"; exit 1; }

# Run one example: make run WEEK=1 EX=10
# calibredrv for weeks >= 21; tclsh for 1–20
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

define RUN_WEEK
	@week_dir="$(LESSONS)/$(1)"; \
	if [ ! -d "$$week_dir" ]; then \
		echo "error: missing $$week_dir — see PLAN.md week $(1); generate with content-generation"; exit 1; \
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
		echo "error: missing $$week_dir — see PLAN.md week $(1)"; exit 1; \
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

# --- helpers to emit weekN-01 .. weekN-12 ---
define WEEK_EX_RULES
week$(1)-01: ; @$$(MAKE) --no-print-directory run WEEK=$(1) EX=01
week$(1)-02: ; @$$(MAKE) --no-print-directory run WEEK=$(1) EX=02
week$(1)-03: ; @$$(MAKE) --no-print-directory run WEEK=$(1) EX=03
week$(1)-04: ; @$$(MAKE) --no-print-directory run WEEK=$(1) EX=04
week$(1)-05: ; @$$(MAKE) --no-print-directory run WEEK=$(1) EX=05
week$(1)-06: ; @$$(MAKE) --no-print-directory run WEEK=$(1) EX=06
week$(1)-07: ; @$$(MAKE) --no-print-directory run WEEK=$(1) EX=07
week$(1)-08: ; @$$(MAKE) --no-print-directory run WEEK=$(1) EX=08
week$(1)-09: ; @$$(MAKE) --no-print-directory run WEEK=$(1) EX=09
week$(1)-10: ; @$$(MAKE) --no-print-directory run WEEK=$(1) EX=10
week$(1)-11: ; @$$(MAKE) --no-print-directory run WEEK=$(1) EX=11
week$(1)-12: ; @$$(MAKE) --no-print-directory run WEEK=$(1) EX=12
endef

week1: check
	$(call RUN_WEEK,1)
$(eval $(call WEEK_EX_RULES,1))

week2: check
	$(call RUN_WEEK,2)
$(eval $(call WEEK_EX_RULES,2))

week3: check
	$(call RUN_WEEK,3)
$(eval $(call WEEK_EX_RULES,3))

week4: check
	$(call RUN_WEEK,4)
$(eval $(call WEEK_EX_RULES,4))

week5: check
	$(call RUN_WEEK,5)
$(eval $(call WEEK_EX_RULES,5))

week6: check
	$(call RUN_WEEK,6)
$(eval $(call WEEK_EX_RULES,6))

week15: check
	$(call RUN_WEEK,15)
$(eval $(call WEEK_EX_RULES,15))

week21: check-calibre
	$(call RUN_WEEK_CALIBRE,21)
$(eval $(call WEEK_EX_RULES,21))

week22: check-calibre
	$(call RUN_WEEK_CALIBRE,22)
$(eval $(call WEEK_EX_RULES,22))

week23: check-calibre
	$(call RUN_WEEK_CALIBRE,23)
$(eval $(call WEEK_EX_RULES,23))

week24: check-calibre
	$(call RUN_WEEK_CALIBRE,24)
$(eval $(call WEEK_EX_RULES,24))

week25: check-calibre
	$(call RUN_WEEK_CALIBRE,25)
$(eval $(call WEEK_EX_RULES,25))

week26: check-calibre
	$(call RUN_WEEK_CALIBRE,26)
$(eval $(call WEEK_EX_RULES,26))

week27: check-calibre
	$(call RUN_WEEK_CALIBRE,27)
$(eval $(call WEEK_EX_RULES,27))

week28: check-calibre
	$(call RUN_WEEK_CALIBRE,28)
$(eval $(call WEEK_EX_RULES,28))

# --- Lesson website (MkDocs → GitHub Pages) ---
site-install:
	pip3 install -r $(ROOT)website/requirements.txt

site:
	python3 $(ROOT)scripts/build_website.py
	cd $(ROOT)website && mkdocs build --strict

site-serve:
	python3 $(ROOT)scripts/build_website.py
	cd $(ROOT)website && mkdocs serve
