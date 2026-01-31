import os
import subprocess
import sys
import shutil

# --- YOL AYARLARI ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "dist")
WORK_DIR = os.path.join(BASE_DIR, "build")

# Version dosyası ana dizinde durmalı (Kaybolmaması için)
VERSION_FILE_SRC = os.path.join(BASE_DIR, "version.txt")
VERSION_FILE_DST = os.path.join(DIST_DIR, "version.txt")

LAUNCHER_SCRIPT = os.path.join(BASE_DIR, "src", "Launcher.py")
GAME_SCRIPT = os.path.join(BASE_DIR, "src", "main.py") 

def ensure_dist_exists():
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)

def get_current_version():
    if not os.path.exists(VERSION_FILE_SRC):
        return 0.0
    with open(VERSION_FILE_SRC, "r") as f:
        try:
            return float(f.read().strip())
        except ValueError:
            return 0.0

def update_version(current_ver):
    ensure_dist_exists()
    new_ver = round(current_ver + 0.01, 2)
    
    # 1. Ana dizindeki dosyayı güncelle (Kalıcılık için)
    with open(VERSION_FILE_SRC, "w") as f:
        f.write(str(new_ver))
    
    # 2. Dist klasörüne kopyala (Dağıtım için)
    shutil.copy(VERSION_FILE_SRC, VERSION_FILE_DST)
    
    print(f"✅ Versiyon güncellendi: {current_ver} -> {new_ver}")
    return new_ver

def build_target(target_name, script_path, console=False):
    ensure_dist_exists()
    print(f"🔨 {target_name} oluşturuluyor...")

    # Mevcut versiyonu dist'e kopyalayalım ki exe yanında bulunsun
    if os.path.exists(VERSION_FILE_SRC):
        shutil.copy(VERSION_FILE_SRC, VERSION_FILE_DST)

    console_option = "--console" if console else "--noconsole"

    # --add-data kullanımı: Eğer assets klasörün varsa buraya eklemelisin!
    # Örnek: "--add-data", f"{os.path.join(BASE_DIR, 'assets')}{os.pathsep}assets",
    
    command = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        console_option,
        "--collect-all", "certifi",
        "--distpath", DIST_DIR,
        "--workpath", WORK_DIR,
        "--log-level", "ERROR",
        "--name", target_name,
        "--clean",
        script_path
    ]
    
    result = subprocess.run(command, capture_output=False)
    
    if result.returncode == 0:
        print(f"🚀 {target_name}.exe başarıyla oluşturuldu!")
    else:
        print(f"❌ {target_name} Build Hatası!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "update":
            ver = get_current_version()
            update_version(ver)
        elif action == "build_launcher":
            build_target("Launcher", LAUNCHER_SCRIPT, console=False)
        elif action == "build_game":
            build_target("game", GAME_SCRIPT, console=True)
        elif action == "build_all":
            build_target("game", GAME_SCRIPT, console=True)
            build_target("Launcher", LAUNCHER_SCRIPT, console=False)
    else:
        print("⚠️ Eksik argüman.")