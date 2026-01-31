from abc import ABC, abstractmethod
import random as rnd

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
        print(f"[{self.name}] Can: {self.hp} | Güç: {self.ad}")

class Hero(Character):
    def __init__(self, name):
        super().__init__(name)
        self.potion = 10
        self.xp = 0
        self.xp_next = 20

    def attack(self, target):
        dice = rnd.randint(1, 20)
        print(f"\n🎲 Zar: {dice}")
        
        if dice < 5:
            print(f"❌ {self.name} Iskaladı!")
        else:
            damage = self.ad * 2 if dice == 20 else self.ad
            target.hp -= damage
            print(f"⚔️ {self.name} -> {target.name} ({damage} hasar)")

    def heal(self):
        if self.potion > 0 and self.hp < 100:
            self.hp = min(100, self.hp + 15)
            self.potion -= 1
            print(f"💚 İyileştin. Can: {self.hp} | Kalan İksir: {self.potion}")
        else:
            print("İksir yok veya canın dolu!")

    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= self.xp_next:
            self.level += 1
            self.ad += 5
            self.xp -= self.xp_next
            self.xp_next += 10
            print(f"🆙 LEVEL UP! Yeni Level: {self.level}")

class Enemy(Character):
    def __init__(self):
        races = ["Goblin", "Ork", "Troll"]
        name = rnd.choice(races)
        super().__init__(name)
        self.hp = rnd.randint(20, 30)
        self.ad = 5
        self.xp_value = 15

    def attack(self, target):
        target.hp -= self.ad
        print(f"👹 {self.name} sana saldırdı! {self.ad} hasar aldın.")