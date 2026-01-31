import os
import subprocess
import sys  # <--- Bunu ekledik, Python'un yerini bulmak için lazım

VERSION_FILE = "version.txt"
GAME_FILE = "RPG.py"

def get_current_version():
    if not os.path.exists(VERSION_FILE):
        return 0.0
    with open(VERSION_FILE, "r") as f:
        try:
            return float(f.read().strip())
        except ValueError:
            return 0.0

def update_version(current_ver):
    new_ver = round(current_ver + 0.01, 2)
    with open(VERSION_FILE, "w") as f:
        f.write(str(new_ver))
    print(f"✅ Versiyon güncellendi: {current_ver} -> {new_ver}")
    return new_ver

def build_exe():
    print("🔨 PyInstaller çalıştırılıyor...")
    
    # --- DEĞİŞİKLİK BURADA ---
    # "pyinstaller" yerine [sys.executable, "-m", "PyInstaller"] kullanıyoruz.
    # Bu, "python -m PyInstaller" komutunun kod halidir.
    command = [sys.executable, "-m", "PyInstaller", "--noconsole", "--onefile", "--log-level", "ERROR", GAME_FILE]
    
    result = subprocess.run(command, capture_output=False)
    
    if result.returncode == 0:
        print("🚀 Build Başarılı! (dist/RPG.exe)")
    else:
        print("❌ Build Hatası!")

if __name__ == "__main__":
    ver = get_current_version()
    update_version(ver)
    build_exe()