# Değişkenler
PYTHON = python
SCRIPT = RPG.py
BUILD_CMD = -m PyInstaller --onefile $(SCRIPT)

# 'make run' yazınca oyunu başlatır
run:
	$(PYTHON) $(SCRIPT)

# DİKKAT: Burayı 'build' yerine 'exe' yaptık ki klasörle karışmasın
exe:
	$(PYTHON) $(BUILD_CMD)

# 'make clean' yazınca temizlik yapar
clean:
	if exist build rmdir /s /q build
	if exist dist rmdir /s /q dist
	if exist *.spec del /q *.spec