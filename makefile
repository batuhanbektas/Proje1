# Değişkenler
PYTHON = python
SCRIPT = src/main.py
MANAGER = src/build_manager.py

# Varsayılan (sadece make yazınca çalışır)
default: all

# 1. HEDEF: make exe -> Sadece oyun
exe:
	$(PYTHON) $(MANAGER) build_game

# 2. HEDEF: make launcher -> Sadece launcher
launcher:
	$(PYTHON) $(MANAGER) build_launcher

# 3. HEDEF: make all -> İkisi birden
all:
	$(PYTHON) $(MANAGER) build_all

# 4. HEDEF: make update -> Versiyonu artırır
update:
	$(PYTHON) $(MANAGER) update

# Test etmek için
run:
	$(PYTHON) $(SCRIPT)

# TEMİZLİK (GÜVENLİ MOD)
# DİKKAT: dist klasörünü komple silmiyoruz ki version.txt kaybolmasın!
clean:
	if exist build rmdir /s /q build
	if exist dist\*.exe del /q dist\*.exe
	if exist *.spec del /q *.spec
	if exist __pycache__ rmdir /s /q __pycache__
	if exist src\__pycache__ rmdir /s /q src\__pycache__