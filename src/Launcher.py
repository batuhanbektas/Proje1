import os
import subprocess
import sys
import shutil

# --- YOL AYARLARI ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSION_FILE = os.path.join(BASE_DIR, "version.txt")
DIST_DIR = os.path.join(BASE_DIR, "dist")
WORK_DIR = os.path.join(BASE_DIR, "build")

# İki farklı hedefimiz var:
LAUNCHER_SCRIPT = os.path.join(BASE_DIR, "src", "Launcher.py")
GAME_SCRIPT = os.path.join(BASE_DIR, "src", "main.py") # Oyunun ana dosyası (main.py veya game.py)

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
    
    # Dist varsa oraya da kopyala
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)
    shutil.copy(VERSION_FILE, os.path.join(DIST_DIR, "version.txt"))

    print(f"✅ Versiyon güncellendi: {current_ver} -> {new_ver}")
    return new_ver

def build_target(target_name, script_path, console=False):
    print(f"🔨 {target_name} için PyInstaller çalıştırılıyor...")

    # Launcher için siyah ekran olmasın (console=False), ama Oyun için olsun (console=True)
    console_option = "--console" if console else "--noconsole"

    command = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        console_option,
        "--collect-all", "certifi", # SSL hatası için gerekli
        "--distpath", DIST_DIR,
        "--workpath", WORK_DIR,
        "--log-level", "ERROR",
        "--name", target_name, # Çıkan exe'nin adı
        script_path
    ]
    
    result = subprocess.run(command, capture_output=False)
    
    if result.returncode == 0:
        print(f"🚀 {target_name}.exe başarıyla oluşturuldu! ({DIST_DIR})")
        # Version dosyasını da yanına koyalım
        if os.path.exists(VERSION_FILE):
             shutil.copy(VERSION_FILE, os.path.join(DIST_DIR, "version.txt"))
    else:
        print(f"❌ {target_name} Build Hatası!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == "update":
            ver = get_current_version()
            update_version(ver)
            
        elif action == "build_launcher":
            # Launcher'ı "Launcher.exe" adıyla üret
            build_target("Launcher", LAUNCHER_SCRIPT, console=False)
            
        elif action == "build_game":
            # Oyunu "RPG.exe" adıyla üret (GitHub'da bu isimle bekliyor)
            build_target("RPG", GAME_SCRIPT, console=True)
            
        elif action == "build_all":
            build_target("Launcher", LAUNCHER_SCRIPT, console=False)
            build_target("RPG", GAME_SCRIPT, console=True)
    else:
        print("⚠️ Komutlar: update, build_launcher, build_game, build_all")