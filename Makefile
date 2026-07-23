VENV_BIN = .venv/bin
UIC = $(VENV_BIN)/pyside6-uic

# Находим все файлы .ui в проекте (включая подпапки, например, ui/)
UI_FILES := ui/mainwindow.ui
PY_FILES := $(patsubst ui/%.ui, ui_%.py, $(UI_FILES))

# Цель по умолчанию (запускается при вызове просто 'make')
.PHONY: all
all: $(PY_FILES)
	@echo "Все файлы интерфейса успешно обновлены!"

ui_%.py: ui/%.ui
	@echo "Компиляция $< -> $@"
	$(UIC) $< -o $@

.PHONY: clean
clean:
	@echo "Удаление сгенерированных файлов интерфейса..."
	rm -f $(PY_FILES)

start:
	$(VENV_BIN)/python3 main.py