# ============================================================
#  Makefile — Yo-kai Watch 2 Decompilation (Nintendo 3DS)
# ============================================================

PYTHON  := python3
TOOLS   := tools
EXTRACT := $(PYTHON) $(TOOLS)/extract_rom.py

.PHONY: all extract info clean distclean

all: info

info:
	@echo "============================================================"
	@echo "  Yo-kai Watch 2: Mentespectros — Decompilación (3DS)"
	@echo "============================================================"
	@echo "Comandos disponibles:"
	@echo "  make extract    - Inspecciona la ROM y descomprime 'code.bin'"
	@echo "  make clean      - Limpia artefactos temporales de compilación"
	@echo "  make distclean  - Elimina también binarios extraídos en 'extracted/'"
	@echo ""
	@if [ -f "extracted/code.raw.bin" ]; then \
		echo "✓ Ejecutable descomprimido presente: extracted/code.raw.bin"; \
	elif [ -f "extracted/code.bin" ]; then \
		echo "✓ Ejecutable 'code.bin' detectado en extracted/"; \
	else \
		echo "⚠️ Pendiente de extraer: ejecuta 'make extract' con la ROM descifrada"; \
	fi

extract:
	@$(EXTRACT)

clean:
	@rm -rf build/
	@echo "Build limpio."

distclean: clean
	@rm -rf extracted/
	@echo "Binarios extraídos eliminados."
