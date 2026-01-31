PYTHON = python
SCRIPT = src/main.py
MANAGER = src/build_manager.py

default: all

exe:
	$(PYTHON) $(MANAGER) build_game

launcher:
	$(PYTHON) $(MANAGER) build_launcher

all:
	$(PYTHON) $(MANAGER) build_all

update:
	$(PYTHON) $(MANAGER) update

run:
	$(PYTHON) $(SCRIPT)

# DİKKAT: Aşağıdaki girintiler TAB olmalı, space değil!
clean:
	if exist build rmdir /s /q build
	if exist dist rmdir /s /q dist
	if exist *.spec del /q *.spec
	if exist __pycache__ rmdir /s /q __pycache__
	if exist src\__pycache__ rmdir /s /q src\__pycache__