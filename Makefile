# ============================================================
#  Makefile — Yo-kai Watch 2 Decompilation (Nintendo 3DS)
# ============================================================

PYTHON   := python3
TOOLS    := tools
EXTRACT  := $(PYTHON) $(TOOLS)/extract_rom.py
PROGRESS := $(PYTHON) $(TOOLS)/audit_progress.py
CHECK    := $(PYTHON) $(TOOLS)/check_match.py

CC       := arm-none-eabi-gcc
AS       := arm-none-eabi-as
CFLAGS   := -c -mcpu=mpcore -O3 -I . -I include

C_SRCS   := $(shell find src -name '*.c' 2>/dev/null)
OBJS     := $(patsubst src/%.c, build/src/%.o, $(C_SRCS))

.PHONY: all extract progress check info clean distclean

all: info

info:
	@echo "============================================================"
	@echo "  Yo-kai Watch 2: Psychic Specters — Decompilation (3DS)"
	@echo "============================================================"
	@echo "Available targets:"
	@echo "  make check      - Compile and verify byte-matching of implemented functions"
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

build/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $< -o $@

clean:
	@rm -rf build/
	@echo "Build cleaned."

distclean: clean
	@rm -rf extracted/
	@echo "Extracted binaries removed."
