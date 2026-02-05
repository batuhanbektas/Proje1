from abc import ABC, abstractmethod
import random as rnd
import time
import json
# Soyut Sınıf (Interface mantığı)
class Character(ABC):
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.ad = rnd.randint(5, 15)
        self.level = 1
    @abstractmethod
    def attack(self, target):
        pass

    def is_alive(self):
        return self.hp > 0

    def info(self):
        pass
class Hero(Character): 
    def __init__(self, name):
        super().__init__(name)
        self.potion = 10
        self.xp = 0
        self.xp_next = 20
        self.size = 10
        self.max_hp = 100
        self.recently_leveled = False
        self.purse = 0

    def level_up(self):
        while True:
            choice = input("""Neyi Geliştirmek istersin: 
                  Seçeneklerin Şunlar:
                  1- Rastgele can artışı 1 ile 20 arasında
                  2- Rastgele hasar artışı 1 ile 5 arasında
                  3- Çanta kapasiten 1 ile 5 arasında
                           """)
            match choice:
                case "1":
                    print(" CAN ARTTIRMAYI SEÇTİN")
                    input("Lütfen zar atmak için bir tuşa bas")
                    print("Zar Atılıyor....")
                    time.sleep(1)
                    dice = rnd.randint(1,20)
                    print(f"Attığın zar {dice}!!! Eski Canın {self.max_hp}")
                    time.sleep(1)
                    self.max_hp += dice
                    print(f"YENİ CANIN: {self.max_hp} ")
                    time.sleep(1)
                    break

                case "2":
                    print(" HASAR ARTTIRMAYI SEÇTİN")
                    input("Lütfen zar atmak için bir tuşa bas")
                    print("Zar Atılıyor....")
                    time.sleep(1)
                    dice = rnd.randint(1,5)
                    print(f"Attığın zar {dice}!!! Eski Hasarın {self.ad}")
                    time.sleep(1)
                    self.ad += dice
                    print(f"YENİ HASARIN: {self.ad} ")
                    time.sleep(1)
                    break
                case "3":
                    print(" ENVANTER ARTTIRMAYI SEÇTİN")
                    input("Lütfen zar atmak için bir tuşa bas")
                    print("Zar Atılıyor....")
                    time.sleep(1)
                    dice = rnd.randint(1,5)
                    print(f"Attığın zar {dice}!!! Eski Envanterin{self.size}")
                    time.sleep(1)
                    self.size += dice
                    print(f"YENİ ENVANTERİN: {self.size} ")
                    time.sleep(1)
                    break
                case _:
                    print("GEÇERSİZ" )          

    def info(self):
        print(f"[{self.name}] Can: {self.hp}/{self.max_hp} | Güç: {self.ad} | Level: {self.level} | XP: {self.xp} | Kalan XP: {self.xp_next - self.xp } | Para: {self.purse}")

    def attack(self, target):
        dice = rnd.randint(1, 20)
        input("Zar atmak için bir tuşa bas: ")
        print("Zar Atılıyor...")
        time.sleep(1)
        if(dice == 20):
            print(f"ZAR 20 , KRİTİK VURDUN")
        else:
            print(f"\n🎲 Zar: {dice}")        
        time.sleep(1)
        
        if dice <= 5:
            print(f"❌ {self.name} Iskaladı!")
            time.sleep(1)
        elif dice >5 and dice != 20:
            target.hp = target.hp - self.ad
            print(f"{self.name} {self.ad} Hasar Vurdu -> {target.name} ") 
            time.sleep(0.5)
        else:
            damage = 2*self.ad
            target.hp = target.hp - damage
            print(f"{self.name} {damage} KRİTİK Hasar Vurdu -> {target.name} ") 
            time.sleep(0.5)

    def heal(self):
        if self.potion > 0 and self.hp < self.max_hp:
            self.hp = min(self.max_hp, self.hp + 15)
            self.potion -= 1
            print(f"💚 İyileştin. Can: {self.hp}/{self.max_hp} | Kalan İksir: {self.potion}")
        else:
            print("İksir yok veya canın dolu!")

    def gain_xp(self, amount):      
        self.xp += amount
        if self.xp >= self.xp_next:
            self.level += 1
            self.xp -= self.xp_next
            self.xp_next += 10
            print(f"🆙 LEVEL UP! Yeni Level: {self.level}")
            time.sleep(1.5)
            self.level_up()
            self.recently_leveled = True

class Enemy(Character):
    def __init__(self):
        races = ["Goblin", "Ork", "Troll"]
        name = rnd.choice(races)
        super().__init__(name)
        self.hp = rnd.randint(20, 30)
        self.ad = 5
        self.xp_value = rnd.randint(10, 20)
        self.value = rnd.randint(5,15)

    def attack(self, target):
        dice = rnd.randint(1, 20)
        if dice <= 5:
            print(f"❌ {self.name} Iskaladı!")
        else:
            target.hp -= self.ad
            print(f"👹 {self.name} sana saldırdı! {self.ad} hasar aldın.")
    
    def info(self):
           print(f"[{self.name}] Can: {self.hp} | Güç: {self.ad} | XP: {self.xp_value}")
        
class Boss(Enemy):
    def __init__(self):
        bosses = ["Dragon", "Demon Lord", "Giant"]
        name = rnd.choice(bosses)
        super().__init__()
        self.name = name
        self.hp = rnd.randint(100, 150)
        self.ad = rnd.randint(15, 25)
        self.xp_value = rnd.randint(50, 100)
        self.value = rnd.randint(50,100)