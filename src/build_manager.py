import os
import subprocess
import sys

# --- YOL AYARLARI ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "dist")
WORK_DIR = os.path.join(BASE_DIR, "build")

# İSTEĞİN ÜZERİNE: Versiyon dosyası artık sadece DIST içinde aranıyor
VERSION_FILE = os.path.join(DIST_DIR, "version.txt")

# Hedef scriptler
LAUNCHER_SCRIPT = os.path.join(BASE_DIR, "src", "Launcher.py")
GAME_SCRIPT = os.path.join(BASE_DIR, "src", "main.py") 

def ensure_dist_exists():
    """Dist klasörü yoksa oluşturur."""
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)

def get_current_version():
    ensure_dist_exists()
    if not os.path.exists(VERSION_FILE):
        return 0.0
    with open(VERSION_FILE, "r") as f:
        try:
            return float(f.read().strip())
        except ValueError:
            return 0.0

def update_version(current_ver):
    ensure_dist_exists()
    new_ver = round(current_ver + 0.01, 2)
    
    # Doğrudan dist/version.txt güncelleniyor
    with open(VERSION_FILE, "w") as f:
        f.write(str(new_ver))
    
    print(f"✅ Versiyon güncellendi (dist): {current_ver} -> {new_ver}")
    return new_ver

def build_target(target_name, script_path, console=False):
    ensure_dist_exists()
    print(f"🔨 {target_name} oluşturuluyor...")

    console_option = "--console" if console else "--noconsole"

    command = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        console_option,
        "--collect-all", "certifi",
        "--distpath", DIST_DIR,
        "--workpath", WORK_DIR,
        "--log-level", "ERROR",
        "--name", target_name,
        "--clean", # Önbelleği temizle
        script_path
    ]
    
    result = subprocess.run(command, capture_output=False)
    
    if result.returncode == 0:
        print(f"🚀 {target_name}.exe başarıyla oluşturuldu!")
        # Version dosyası zaten dist içinde olduğu için kopyalamaya gerek yok
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
            build_target("RPG", GAME_SCRIPT, console=True)
            
        elif action == "build_all":
            build_target("RPG", GAME_SCRIPT, console=True)
            build_target("Launcher", LAUNCHER_SCRIPT, console=False)
    else:
        print("⚠️ Eksik argüman. makefile üzerinden çalıştırın.")