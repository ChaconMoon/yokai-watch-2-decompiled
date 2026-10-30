# ============================================================
#  Makefile — Yo-kai Watch 2 Decompilation (Nintendo 3DS)
# ============================================================

PYTHON   := python3
TOOLS    := tools
EXTRACT  := $(PYTHON) $(TOOLS)/extract_rom.py
PROGRESS := $(PYTHON) $(TOOLS)/audit_progress.py
CLASSES  := $(PYTHON) $(TOOLS)/extract_classes.py
CHECK    := $(PYTHON) $(TOOLS)/check_match.py
DUMP     := $(PYTHON) $(TOOLS)/dump_asm.py
INJECT   := $(PYTHON) $(TOOLS)/inject_code.py
LIVE     := $(PYTHON) $(TOOLS)/export_live.py
AZAHAR_MOD_DIR := $(HOME)/.local/share/azahar-emu/load/mods/00040000001B2900/exefs

CC       := arm-none-eabi-gcc
CXX      := arm-none-eabi-g++
AS       := arm-none-eabi-as
ASFLAGS  := -mcpu=mpcore -mfpu=vfpv2
CFLAGS   := -c -mcpu=mpcore -O3 -I . -I include
CXXFLAGS := -c -mcpu=mpcore -O3 -I . -I include -fno-rtti -fno-exceptions

C_SRCS   := $(shell find src -name '*.c' 2>/dev/null)
CPP_SRCS := $(shell find src -name '*.cpp' 2>/dev/null)
S_SRCS   := $(shell find src -name '*.s' 2>/dev/null)
OBJS     := $(patsubst src/%.c, build/src/%.o, $(C_SRCS)) \
            $(patsubst src/%.cpp, build/src/%.o, $(CPP_SRCS)) \
            $(patsubst src/%.s, build/src/%.o, $(S_SRCS))

.PHONY: all build extract progress classes check inject dump report info clean distclean live hooks

all: build

build: $(OBJS)

report: $(OBJS)
	@mkdir -p build expected
	@python3 tools/generate_report.py

hooks:
	@mkdir -p .git/hooks tools/hooks
	@chmod +x tools/hooks/pre-commit tools/hooks/pre-push
	@cp tools/hooks/pre-commit .git/hooks/pre-commit
	@cp tools/hooks/pre-push .git/hooks/pre-push
	@chmod +x .git/hooks/pre-commit .git/hooks/pre-push
	@git config core.hooksPath tools/hooks 2>/dev/null || true
	@echo "✅ Git pre-commit y pre-push hooks instalados y configurados correctamente."

info:
	@echo "============================================================"
	@echo "  Yo-kai Watch 2: Psychic Specters — Decompilation (3DS)"
	@echo "============================================================"
	@echo "Available targets:"
	@echo "  make check      - Compile and verify byte-matching of implemented functions"
	@echo "  make hooks      - Install Git pre-commit & pre-push hooks (CI & README checks)"
	@echo "  make inject     - Build 'build/code.bin' and install to Azahar emulator mods"
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
	@if [ -f "extracted/code.raw.bin" ]; then \
		$(PYTHON) $(TOOLS)/generate_expected.py >/dev/null; \
	fi
	@$(PROGRESS) --update-readme
	@$(LIVE)

live:
	@$(LIVE)

classes:
	@$(CLASSES)

check: $(OBJS)
	@$(CHECK)

inject: $(OBJS)
	@$(INJECT)
	@if [ -d "$(AZAHAR_MOD_DIR)" ]; then \
		cp build/code.bin "$(AZAHAR_MOD_DIR)/code.bin"; \
		echo "✅ Installed build/code.bin -> $(AZAHAR_MOD_DIR)/code.bin"; \
	fi

dump:
	@if [ -z "$(FUNC)" ]; then \
		echo "Usage: make dump FUNC=<address_or_symbol> [e.g. make dump FUNC=0x0010B6D8]"; \
	else \
		$(DUMP) $(FUNC) --plain; \
	fi


build/src/ctr/nn/os/func_00104D18.o: CFLAGS += -ffixed-r3 -ffixed-r2
build/src/ctr/nn/os/func_001063F4.o: CFLAGS += -ffixed-r3 -ffixed-r2 -ffixed-r1
build/src/ctr/nn/os/func_0010655C.o: CFLAGS += -ffixed-r3 -ffixed-r2
build/src/ctr/nn/os/func_0010678C.o: CFLAGS += -ffixed-r3 -ffixed-r2 -ffixed-r1
build/src/ctr/nn/os/func_0012788C.o: CFLAGS += -ffixed-r3 -ffixed-r2
build/src/ctr/nn/ndm/func_001280A8.o: CFLAGS += -ffixed-r3
build/src/ctr/nn/dsp/func_00137054.o: CFLAGS += -ffixed-r3 -ffixed-r2 -ffixed-r1
build/src/ctr/nn/dsp/func_001389BC.o: CFLAGS += -ffixed-r3 -ffixed-r2 -ffixed-r1
build/src/ctr/nn/dsp/func_00138A80.o: CFLAGS += -ffixed-r3 -ffixed-r2 -ffixed-r1
build/src/ctr/nn/dsp/func_00138A90.o: CFLAGS += -ffixed-r3 -ffixed-r2 -ffixed-r1
build/src/engine/lfw/func_0010BBB8.o: CFLAGS += -ffixed-r3 -ffixed-r2
build/src/engine/lfw/func_0010C598.o: CFLAGS += -ffixed-r3 -ffixed-r2 -ffixed-r1
build/src/engine/lfw/func_0010C5C8.o: CFLAGS += -ffixed-r3 -ffixed-r2
build/src/engine/lfw/func_0010C6A4.o: CFLAGS += -ffixed-r3 -ffixed-r2
build/src/game/loops/func_0010C870.o: CFLAGS += -ffixed-r3 -ffixed-r2
build/src/game/loops/func_0010C8A0.o: CFLAGS += -ffixed-r3 -ffixed-r2
build/src/game/loops/func_0010CA68.o: CFLAGS += -ffixed-r3 -ffixed-r2

WIBO     := tools/wibo
ARMCC    := $(WIBO) tools/armcc/4.0/b821/bin/armcc.exe
ARMFLAGS := --cpu=mpcore -O3 --gnu -c -I . -I include
build/src/ctr/nn/nex/qResult.o: ARMFLAGS += -Otime
build/src/ctr/nn/applet/applet.o: ARMFLAGS += --split_sections

build/src/ctr/nn/os/func_00106504.o: ARMFLAGS += -Otime
build/src/ctr/nn/os/func_00106504.o: src/ctr/nn/os/func_00106504.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/os/func_00106518.o: ARMFLAGS += -Otime
build/src/ctr/nn/os/func_00106518.o: src/ctr/nn/os/func_00106518.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/game/loops/func_0010C880.o: ARMFLAGS += -Otime
build/src/game/loops/func_0010C880.o: src/game/loops/func_0010C880.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/game/loops/func_0011054C.o: src/game/loops/func_0011054C.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_00136318.o: src/ctr/nn/dsp/func_00136318.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_0013636C.o: ARMFLAGS := --cpu=mpcore -O2 -Otime --gnu -c -I . -I include
build/src/ctr/nn/dsp/func_0013636C.o: src/ctr/nn/dsp/func_0013636C.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_00136420.o: ARMFLAGS := --cpu=mpcore -O1 --gnu -c -I . -I include
build/src/ctr/nn/dsp/func_00136420.o: src/ctr/nn/dsp/func_00136420.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_00136804.o: ARMFLAGS := --cpu=mpcore -O2 -Otime --gnu -c -I . -I include
build/src/ctr/nn/dsp/func_00136804.o: src/ctr/nn/dsp/func_00136804.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_001375DC.o: src/ctr/nn/dsp/func_001375DC.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_00137920.o: src/ctr/nn/dsp/func_00137920.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_00137930.o: src/ctr/nn/dsp/func_00137930.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_00137A0C.o: src/ctr/nn/dsp/func_00137A0C.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_00137F18.o: src/ctr/nn/dsp/func_00137F18.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_00137F28.o: src/ctr/nn/dsp/func_00137F28.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_00137F40.o: src/ctr/nn/dsp/func_00137F40.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_0013810C.o: src/ctr/nn/dsp/func_0013810C.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_001385D0.o: ARMFLAGS += -Otime
build/src/ctr/nn/dsp/func_001385D0.o: src/ctr/nn/dsp/func_001385D0.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_001386D4.o: src/ctr/nn/dsp/func_001386D4.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_001388CC.o: src/ctr/nn/dsp/func_001388CC.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_00138AA0.o: src/ctr/nn/dsp/func_00138AA0.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_00138AAC.o: src/ctr/nn/dsp/func_00138AAC.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/dsp/func_00138B58.o: src/ctr/nn/dsp/func_00138B58.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/y2r/%.o: src/ctr/nn/y2r/%.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/y2r/func_00112E60.o: src/ctr/nn/y2r/func_00112E60.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) --cpu=arm1136j-s $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/y2r/func_001137C0.o: src/ctr/nn/y2r/func_001137C0.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/y2r/func_00113F58.o: src/ctr/nn/y2r/func_00113F58.c
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) $< -o $@; \
	else \
		echo "⚠️ Warning: ARMCC not found, compiling with GCC fallback..."; \
		$(CC) $(CFLAGS) $< -o $@; \
	fi

build/src/ctr/nn/y2r/func_00113F70.o: src/ctr/nn/y2r/func_00113F70.c
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

build/%.o: %.cpp
	@mkdir -p $(dir $@)
	@if [ -f "tools/armcc/4.0/b821/bin/armcc.exe" ]; then \
		$(ARMCC) $(ARMFLAGS) --cpp $< -o $@; \
	else \
		$(CXX) $(CXXFLAGS) $< -o $@; \
	fi

build/%.o: %.s
	@mkdir -p $(dir $@)
	$(AS) $(ASFLAGS) $< -o $@

clean:
	@rm -rf build/
	@echo "Build cleaned."

distclean: clean
	@rm -rf extracted/
	@echo "Extracted binaries removed."
