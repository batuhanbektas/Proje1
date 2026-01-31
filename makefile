# Değişkenler
PYTHON = python
SCRIPT = RPG.py
# Yeni build yöneticisi scriptimiz
MANAGER = build_manager.py

# Varsayılan hedef: Sadece 'make' yazarsan direkt exe oluşturur
all: exe

# 'make run' yazınca oyunu normal python ile başlatır (hızlı test için)
run:
	$(PYTHON) $(SCRIPT)

# 'make exe' yazınca: 
# 1. build_manager.py çalışır
# 2. Version.txt güncellenir (örn: 0.05 -> 0.06)
# 3. Otomatik olarak PyInstaller çalıştırılır
exe:
	$(PYTHON) $(MANAGER)

# 'make clean' yazınca gereksiz dosyaları temizler
clean:
	if exist build rmdir /s /q build
	if exist dist rmdir /s /q dist
	if exist *.spec del /q *.spec
	if exist __pycache__ rmdir /s /q __pycache__