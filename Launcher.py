import tkinter as tk
from tkinter import messagebox, ttk
import requests
import os
import subprocess
import threading

# --- SENİN LİNKLERİN ---
VERSION_URL = "https://github.com/batuhanbektas/Proje1/raw/refs/heads/main/version.txt"
GAME_URL = "https://github.com/batuhanbektas/Proje1/raw/refs/heads/main/dist/RPG.exe"

# Bilgisayara bu isimle inecek (Repo'daki isimle aynı yaptım)
GAME_FILENAME = "RPG.exe" 
LOCAL_VERSION_FILE = "version.txt" 

class LauncherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RPG Oyun Launcher")
        self.root.geometry("300x250")
        self.root.resizable(False, False)

        # Başlık
        self.label = tk.Label(root, text="RPG OYUNU", font=("Helvetica", 16, "bold"))
        self.label.pack(pady=20)

        # Durum Mesajı
        self.status_label = tk.Label(root, text="Kontrol ediliyor...", fg="gray")
        self.status_label.pack(pady=5)

        # Progress Bar (Yükleme çubuğu)
        self.progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        self.progress.pack(pady=10)

        # Butonlar
        self.play_button = tk.Button(root, text="OYNA", command=self.launch_game, state="disabled", bg="green", fg="white", font=("Arial", 12))
        self.play_button.pack(pady=5)

        self.update_button = tk.Button(root, text="GÜNCELLE", command=self.start_update, state="disabled", bg="orange", fg="white", font=("Arial", 12))
        self.update_button.pack(pady=5)

        # Başlangıçta versiyonu kontrol et
        threading.Thread(target=self.check_updates).start()

    def get_local_version(self):
        # Eğer bilgisayarda version.txt varsa oku, yoksa 0.0 döndür
        if os.path.exists(LOCAL_VERSION_FILE):
            with open(LOCAL_VERSION_FILE, "r") as f:
                return f.read().strip()
        return "0.0"

    def check_updates(self):
        try:
            self.status_label.config(text="Sunucuya bağlanılıyor...")
            
            # 1. GitHub'daki versiyonu öğren
            response = requests.get(VERSION_URL)
            if response.status_code != 200:
                raise Exception("Versiyon dosyası okunamadı.")
                
            remote_version = response.text.strip()
            
            # 2. Bilgisayardaki versiyonu öğren
            local_version = self.get_local_version()

            print(f"Sunucu: {remote_version} | Yerel: {local_version}") # Konsol kontrolü için

            # 3. Karşılaştır
            if remote_version > local_version:
                self.status_label.config(text=f"Yeni güncelleme var! (v{remote_version})", fg="red")
                self.update_button.config(state="normal") # Güncelle butonu aktif
            else:
                self.status_label.config(text=f"Oyun Güncel (v{local_version})", fg="green")
                # Eğer oyun dosyası fiziksel olarak varsa Oyna butonu aktif
                if os.path.exists(GAME_FILENAME):
                    self.play_button.config(state="normal")
                else:
                    self.status_label.config(text=f"Oyun dosyası eksik! Güncelleyin.", fg="orange")
                    self.update_button.config(state="normal")
                
        except Exception as e:
            self.status_label.config(text="Sunucu hatası!", fg="red")
            print(e)
            # Hata olsa bile oyun varsa oyna butonunu açalım (Offline mod gibi)
            if os.path.exists(GAME_FILENAME):
                self.play_button.config(state="normal")

    def start_update(self):
        self.update_button.config(state="disabled")
        self.play_button.config(state="disabled")
        # İndirme işlemini arayüzü dondurmamak için thread içinde yapıyoruz
        threading.Thread(target=self.download_game).start()

    def download_game(self):
        try:
            self.status_label.config(text="İndiriliyor...")
            
            # Oyunu indir (Streaming ile progress bar için)
            response = requests.get(GAME_URL, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024 # 1 KB
            
            with open(GAME_FILENAME, 'wb') as file:
                downloaded = 0
                for data in response.iter_content(block_size):
                    file.write(data)
                    downloaded += len(data)
                    # Progress bar güncelle
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        self.progress['value'] = percent
                        self.root.update_idletasks()

            # İndirme bitince GitHub'daki versiyonu yerel dosyaya kaydet
            response_ver = requests.get(VERSION_URL)
            with open(LOCAL_VERSION_FILE, "w") as f:
                f.write(response_ver.text.strip())

            self.status_label.config(text="Güncelleme Tamamlandı!", fg="green")
            self.play_button.config(state="normal")
            messagebox.showinfo("Başarılı", "Oyun başarıyla güncellendi! İyi eğlenceler.")

        except Exception as e:
            self.status_label.config(text="İndirme Hatası", fg="red")
            messagebox.showerror("Hata", f"Güncelleme sırasında hata oluştu:\n{e}")

    def launch_game(self):
        if os.path.exists(GAME_FILENAME):
            self.root.destroy() # Launcher'ı kapat
            subprocess.Popen([GAME_FILENAME]) # Oyunu aç
        else:
            messagebox.showerror("Hata", f"{GAME_FILENAME} bulunamadı!")

if __name__ == "__main__":
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()