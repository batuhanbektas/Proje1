import time
from src.models import Hero, Enemy

class Game:
    def __init__(self):
        self.is_running = True
        name = input("Kahramanın adı: ")
        self.player = Hero(name)
        self.enemy = None
    
    def shop_menu(self):
        while True:
            print("\n--- MAĞAZA ---")
            print(f"İksirlerin: {self.player.potion}")
            choice = input("1-İksir Al (Satın al) \n2-Çıkış\nSeçim: ")
            
            match choice:
                case "1":
                    if self.player.potion < 10:
                        self.player.potion += 1
                        print("İksir alındı.")
                    else:
                        print("Çanta dolu!")
                case "2":
                    break
                case _:
                    print("Geçersiz işlem.")

    def battle_phase(self):
        # Düşman yoksa yeni yarat
        if not self.enemy or not self.enemy.is_alive():
            self.enemy = Enemy()
            print(f"\n⚠️ Vahşi bir {self.enemy.name} belirdi!")

        print("-" * 30)
        self.player.info()
        self.enemy.info()
        print("-" * 30)

        print("1. Saldır | 2. İyileş | 3. Mağaza | 4. Çık")
        choice = input("Kararın: ")

        match choice:
            case "1":
                self.player.attack(self.enemy)
                if self.enemy.is_alive():
                    self.enemy.attack(self.player)
                else:
                    print(f"💀 {self.enemy.name} öldü!")
                    self.player.gain_xp(self.enemy.xp_value)
                    self.enemy = None # Düşmanı sıfırla
            case "2":
                self.player.heal()
                if self.enemy and self.enemy.is_alive():
                    self.enemy.attack(self.player)
            case "3":
                # Savaş ortasında mağazaya girmek ister misin? 
                # Mantıken savaş bitince açılması daha iyi ama senin koduna sadık kaldım.
                self.shop_menu()
            case "4":
                self.is_running = False
            case _:
                print("Geçersiz hamle.")

        if not self.player.is_alive():
            print("💀 ÖLDÜN! GAME OVER.")
            self.is_running = False

    def start(self):
        while self.is_running:
            self.battle_phase()
            # Küçük bir bekleme süresi, akışın çok hızlı olmaması için
            time.sleep(1)