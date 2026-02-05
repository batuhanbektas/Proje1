import time
from models import Hero, Enemy, Boss
import random as rnd

class Game:
    def __init__(self):
        self.is_running = True
        self.player = None
        self.enemy = None
        self.set_name()


    def set_name(self):
        i = 0
        banned = ["nigger", "NIGGER", "zigger", "ZIGGER", "nigga", "NIGGA", "zigga", "ZIGGA", "zenci", "ZENCİ", "digger", "DIGGER", "Digger", "diger", "DİGER", "Diger", "Diger ", "Bigger", "bigger", "BİGGER", "bİgger"]
        while True:
            name = input("Kahramanın Adı: ")
            if name in banned and name:
                i += 1  
                if i<3:
                    print("BU ISMI YAPAMAZSIN YARRAK KAFA OMER")
                elif 3 <= i < 5:
                    print("HAHAHHAHAHAHAHAHAHH MAL AMK")
                else:
                    print("denicen mi boyle sonsuza kadar")        
            else:
                self.player = Hero(name)
                return self.player



    def shop_menu(self):
        while True:
            print("\n--- MAĞAZA ---")
            print(f"İksirlerin: {self.player.potion}")
            choice = input("1-İksir Al (Satın al) \n2-Çıkış\nSeçim: ")
            
            match choice:
                case "1":
                    if self.player.potion < self.player.size and self.player.purse >= 10:
                        self.player.potion += 1
                        self.player.purse -= 10
                        print("İksir alındı. Kalan para: ", self.player.purse)
                    else:
                        print("Çanta dolu ya da yeterli paran yok!")
                        time.sleep(1)
                case "2":
                    break
                case _:
                    print("Geçersiz işlem.")
        

    def battle_phase(self):
        # Düşman yoksa yeni yarat
        if self.player.recently_leveled:
            print("Seviyen yükseldi! Yeni düşman geliyor...")
            time.sleep(2)
            self.enemy = Boss()  # Boss düşmanı yarat
            self.player.recently_leveled = False
        elif not self.enemy or not self.enemy.is_alive():
            self.enemy = Enemy()
            print(f"\n⚠️ Vahşi bir {self.enemy.name} belirdi!")
            time.sleep(1)

        print("-" * 30)
        self.player.info()
        self.enemy.info()
        print("-" * 30)

        print("1. Saldır | 2. İyileş  | 3. Çık")
        choice = input("Kararın: ")

        match choice:
            case "1":
                self.player.attack(self.enemy)
                if self.enemy.is_alive():
                    self.enemy.attack(self.player)
                else:
                    print(f"💀 {self.enemy.name} öldü! Kazandigin XP: {self.enemy.xp_value}, Kazandigin Gold: {self.enemy.value}")
                    self.player.purse += self.enemy.value
                    self.player.gain_xp(self.enemy.xp_value)
                    self.enemy = None # Düşmanı sıfırla

                    print("Mağazaya uğramak ister misin:")
                    karar = input("1 - Evet ||| 2 - Hayır")
                    while True:
                        if karar=="1":
                            self.shop_menu()
                            break
                        elif karar =="2":
                            break
                        else:
                            print("GEÇERSİZ")

            case "2":
                self.player.heal()
                if self.enemy and self.enemy.is_alive():
                    self.enemy.attack(self.player)
            case "3":
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