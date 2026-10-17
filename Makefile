# ============================================================
#  Makefile — Yo-kai Watch 2 Decompilation (Nintendo 3DS)
# ============================================================

PYTHON   := python3
TOOLS    := tools
EXTRACT  := $(PYTHON) $(TOOLS)/extract_rom.py
PROGRESS := $(PYTHON) $(TOOLS)/audit_progress.py
CHECK    := $(PYTHON) $(TOOLS)/check_match.py
DUMP     := $(PYTHON) $(TOOLS)/dump_asm.py

CC       := arm-none-eabi-gcc
AS       := arm-none-eabi-as
ASFLAGS  := -mcpu=mpcore
CFLAGS   := -c -mcpu=mpcore -O3 -I . -I include

C_SRCS   := $(shell find src -name '*.c' 2>/dev/null)
S_SRCS   := $(shell find src -name '*.s' 2>/dev/null)
OBJS     := $(patsubst src/%.c, build/src/%.o, $(C_SRCS)) $(patsubst src/%.s, build/src/%.o, $(S_SRCS))

.PHONY: all build extract progress check dump report info clean distclean

all: build

build: $(OBJS)

report: $(OBJS)
	@mkdir -p build expected
	@python3 tools/generate_undecompiled.py
	@if [ -f "./tools/objdiff-cli" ]; then \
		./tools/objdiff-cli report generate -o build/report.json; \
	else \
		echo "⚠️ objdiff-cli not found. Download it to tools/objdiff-cli first."; \
	fi

info:
	@echo "============================================================"
	@echo "  Yo-kai Watch 2: Psychic Specters — Decompilation (3DS)"
	@echo "============================================================"
	@echo "Available targets:"
	@echo "  make check      - Compile and verify byte-matching of implemented functions"
	@echo "  make dump       - Dump clean assembly for decomp.me (e.g. make dump FUNC=0x0010B6D8)"
	@echo "  make progress   - Audit progress and update README tables"
	@echo "  make extract    - Inspect ROM and decompress 'code.bin'"
	@echo "  make clean      - Clean temporary build artifacts"
	@echo "  make distclean  - Also remove extracted binaries in 'extracted/'"
	@echo ""
	@if [ -f "extracted/code.raw.bin" ]; then \
		echo "✓ Decompressed executable present: extracted/code.raw.bin"; \
	elif [ -f "extracted/code.bin" ]; then \
		echo "✓ Executable 'code.bin' detected in extracted/"; \
	else \
		echo "⚠️ Extraction pending: run 'make extract' with a decrypted ROM"; \
	fi

extract:
	@$(EXTRACT)

progress:
	@$(PROGRESS) --update-readme

check: $(OBJS)
	@$(CHECK)

dump:
	@if [ -z "$(FUNC)" ]; then \
		echo "Usage: make dump FUNC=<address_or_symbol> [e.g. make dump FUNC=0x0010B6D8]"; \
	else \
		$(DUMP) $(FUNC) --plain; \
	fi


build/src/ctr/nn/os/func_00104D18.o: CFLAGS += -ffixed-r3 -ffixed-r2
build/src/ctr/nn/os/func_001063F4.o: CFLAGS += -ffixed-r3 -ffixed-r2 -ffixed-r1
build/src/ctr/nn/os/func_0010678C.o: CFLAGS += -ffixed-r3 -ffixed-r2 -ffixed-r1

WIBO     := tools/wibo
ARMCC    := $(WIBO) tools/armcc/4.0/b821/bin/armcc.exe
ARMFLAGS := --cpu=mpcore -O3 -c -I . -I include

build/src/game/loops/func_0011054C.o: src/game/loops/func_0011054C.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/os/func_001274A0.o: src/ctr/nn/os/func_001274A0.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $< -o $@

build/%.o: %.s
	@mkdir -p $(dir $@)
	$(AS) $(ASFLAGS) $< -o $@

clean:
	@rm -rf build/
	@echo "Build cleaned."

distclean: clean
	@rm -rf extracted/
	@echo "Extracted binaries removed."
