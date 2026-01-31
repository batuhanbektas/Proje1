# Değişkenler
PYTHON = python
# Yolları güncelledik: src/ klasörünü ekledik
MANAGER = src/build_manager.py
SCRIPT = src/main.py

# Varsayılan hedef
all: exe

# Hızlı test (main.py'yi çalıştırır)
run:
	$(PYTHON) $(SCRIPT)

# Sadece versiyon yükselt
update:
	$(PYTHON) $(MANAGER) update

# Sadece build al
exe:
	$(PYTHON) $(MANAGER) build

# Versiyon yükselt VE build al
release: update exe

clean:
	if exist build rmdir /s /q build
	if exist dist rmdir /s /q dist
	if exist *.spec del /q *.spec
	if exist __pycache__ rmdir /s /q __pycache__
	if exist src\__pycache__ rmdir /s /q src\__pycache__