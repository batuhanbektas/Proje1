import tkinter as tk
from tkinter import messagebox, ttk
import requests
import os
import subprocess
import threading
import sys
import time

# --- SSL SERTİFİKA HATASI ÇÖZÜMÜ ---
def get_cert_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, 'certifi', 'cacert.pem')
    import certifi
    return certifi.where()

os.environ['REQUESTS_CA_BUNDLE'] = get_cert_path()
# -----------------------------------

# --- AYARLAR ---
# GitHub Raw linklerinin doğru olduğundan emin ol
VERSION_URL = "https://github.com/batuhanbektas/Proje1/raw/refs/heads/main/dist/version.txt"
GAME_URL = "https://github.com/batuhanbektas/Proje1/raw/refs/heads/main/dist/game.exe"

GAME_FILENAME = "game.exe" 
LOCAL_VERSION_FILE = "version.txt" 

class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RPG Oyun Launcher")
        self.root.geometry("300x250")
        self.root.resizable(False, False)

        self.label = tk.Label(root, text="RPG OYUNU", font=("Helvetica", 16, "bold"))
        self.label.pack(pady=20)

        self.status_label = tk.Label(root, text="Kontrol ediliyor...", fg="gray")
        self.status_label.pack(pady=5)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(pady=10)

        self.play_button = tk.Button(root, text="OYNA", command=self.launch_game, state="disabled", bg="green", fg="white", font=("Arial", 12))
        self.play_button.pack(pady=5)

        self.update_button = tk.Button(root, text="GÜNCELLE", command=self.start_update, state="disabled", bg="orange", fg="white", font=("Arial", 12))
        self.update_button.pack(pady=5)

        threading.Thread(target=self.check_updates).start()

    def get_local_version(self):
        if os.path.exists(LOCAL_VERSION_FILE):
            with open(LOCAL_VERSION_FILE, "r") as f:
                return f.read().strip()
        return "0.0"

    def check_updates(self):
        try:
            self.status_label.config(text="Sunucuya bağlanılıyor...")
            
            # Cache Busting (Önbellek Kırma) - Kontrol için
            no_cache_url = f"{VERSION_URL}?t={int(time.time())}"
            response = requests.get(no_cache_url, timeout=5)
            
            if response.status_code != 200:
                raise Exception(f"Hata Kodu: {response.status_code}")
                
            remote_version = response.text.strip()
            local_version = self.get_local_version()

            # --- AJAN KOD (Bunu ekle ki görelim) ---
            messagebox.showinfo("DEBUG BİLGİSİ", 
                                f"İstek Yapılan URL:\n{no_cache_url}\n\n"
                                f"Sunucudan Gelen Veri: '{remote_version}'\n"
                                f"Bilgisayardaki Veri: '{local_version}'")
            # ---------------------------------------

            
            print(f"Sunucu: {remote_version} | Yerel: {local_version}")

            if float(remote_version) > float(local_version):
                self.status_label.config(text=f"Yeni güncelleme: v{remote_version}", fg="red")
                self.update_button.config(state="normal")
            else:
                self.status_label.config(text=f"Oyun Güncel (v{local_version})", fg="green")
                if os.path.exists(GAME_FILENAME):
                    self.play_button.config(state="normal")
                else:
                    self.status_label.config(text="Oyun dosyası eksik!", fg="orange")
                    self.update_button.config(state="normal")
                
        except Exception as e:
            print(f"Hata Detayı: {e}")
            self.status_label.config(text="Sunucu hatası!", fg="red")
            # İnternet yoksa ama oyun varsa yine de oynamaya izin ver
            if os.path.exists(GAME_FILENAME):
                self.play_button.config(state="normal")

    def start_update(self):
        self.update_button.config(state="disabled")
        self.play_button.config(state="disabled")
        threading.Thread(target=self.download_game).start()

    def download_game(self):
        try:
            self.status_label.config(text="İndiriliyor...")
            
            # 1. Oyunu İndir
            response = requests.get(GAME_URL, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(GAME_FILENAME, 'wb') as file:
                downloaded = 0
                for data in response.iter_content(1024):
                    file.write(data)
                    downloaded += len(data)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        self.progress['value'] = percent
                        self.root.update_idletasks()

            # 2. Versiyonu Güncelle (Cache Busting ile)
            no_cache_url = f"{VERSION_URL}?t={int(time.time())}"
            ver_response = requests.get(no_cache_url)
            
            with open(LOCAL_VERSION_FILE, "w") as f:
                f.write(ver_response.text.strip())

            self.status_label.config(text="Güncelleme Tamamlandı!", fg="green")
            self.play_button.config(state="normal")
            messagebox.showinfo("Başarılı", "Oyun başarıyla indirildi/güncellendi!")

        except Exception as e:
            self.status_label.config(text="İndirme Hatası", fg="red")
            messagebox.showerror("Hata", str(e))

    def launch_game(self):
        if os.path.exists(GAME_FILENAME):
            self.root.destroy() # Launcher kapanır
            subprocess.Popen([GAME_FILENAME]) # Oyun açılır
        else:
            messagebox.showerror("Hata", "Oyun dosyası bulunamadı!")

if __name__ == "__main__":
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()