import os
import subprocess
import sys

# Dosya yollarını ayarlıyoruz
# Build manager artık src içinde olduğu için, bir üst klasöre (..) çıkıp bakmalı
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_FILE = os.path.join(BASE_DIR, "version.txt")

# Oyun dosyasının yeri de artık src içinde (kendi yanı başında)
# NOT: Senin ana oyun dosyan hangisiyse ismini ona göre düzelt (RPG.py, game.py veya Launcher.py)
GAME_FILE = os.path.join(BASE_DIR, "src", "Launcher.py") 

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
    
    # --distpath ile exe'nin nereye çıkacağını açıkça belirtiyoruz (Proje ana dizinindeki dist'e)
    dist_path = os.path.join(BASE_DIR, "dist")
    work_path = os.path.join(BASE_DIR, "build")
    
    command = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole", # Launcher için siyah ekranı kapatır (İsteğe bağlı)
        "--collect-all", "certifi",  # <--- KRİTİK EKLEME BURASI
        "--distpath", dist_path,
        "--workpath", work_path,
        "--log-level", "ERROR",
        "--name", "Launcher",  # Çıkan dosyanın adı Launcher.exe olsun
        GAME_FILE
    ]   
    
    result = subprocess.run(command, capture_output=False)
    
    if result.returncode == 0:
        print(f"🚀 Build Başarılı! ({dist_path}/RPG.exe)")
    else:
        print("❌ Build Hatası!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "update":
            ver = get_current_version()
            update_version(ver)
        elif action == "build":
            build_exe()
    else:
        print("⚠️ Lütfen 'update' veya 'build' komutu verin.")