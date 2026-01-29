import random as rnd


class Character:
    def __init__(self, name="none"): # Varsayılan isim atadık
        self.hp = 100
        self.ad = rnd.randint(5, 15) # Hasarı biraz artırdım
        self.name = name
    
    def Info(self):
        print(f"[{self.name}] Can: {self.hp} | Güç: {self.ad}")




class Hero(Character):
  
    def Attack(self, target):
        dice = rnd.randint(1, 20)
        print(f"\n🎲 Zar Attın: {dice}")
        
        if dice < 5:
            print(f"❌ {self.name} Iskaladı!")
        elif dice == 20:
            damage = 2 * self.ad
            target.hp -= damage
            print(f"🔥 KRİTİK VURUŞ! {target.name} isimli düşmana {damage} hasar verdin!")
        else:
            damage = self.ad
            target.hp -= damage
            print(f"⚔️ {self.name}, {target.name} hedefine {damage} hasar verdi.")
        
    def Heal(self):
        if(self.hp==100):
            pass
        else:
            self.hp += 15 # Değer ataması düzeltildi (+=)
            if(self.hp >= 100):
                self.hp = 100
        print(f"💚 {self.name} iyileşti. Yeni Can: {self.hp}")

class Enemy(Character):
    def __init__(self):
        # Önce rastgele bir ırk seçelim
        races = ["Goblin", "Ork", "Blight", "Troll"]
        race_name = rnd.choice(races)
        
        # ŞİMDİ üst sınıfın (Character) özelliklerini çağırıyoruz
        # super().__init__(name) diyerek ismi yukarıya gönderiyoruz
        super().__init__(name=race_name)
        
        # Düşmanın canını kahramandan biraz daha az yapabiliriz (isteğe bağlı)
        self.hp = rnd.randint(50, 80)

    # Attack ve Info metodların aynen kalabilir...
    def Attack(self, target):
        damage = self.ad
        target.hp -= damage
        print(f"👹 {self.name} sana saldırdı! {damage} hasar aldın.")
        
# --- OYUN BAŞLIYOR ---

isim = input("Kahramanın adı ne olsun?: ")
player = Hero(isim)
creature = Enemy()

print(f"\nKarşına vahşi bir {creature.name} çıktı!")

while True:
    print("-" * 30)
    player.Info()
    creature.Info()
    print("-" * 30)
    
    # Can kontrolü (Eksiye düşerse döngüyü kır)
    if player.hp <= 0:
        print("\n💀 ÖLDÜN! Oyun Bitti.")
        break
    if creature.hp <= 0:
        print(f"\n🏆 KAZANDIN! {creature.name} öldü.")
        break

    print("\nNe yapacaksın?")
    print("1. Saldır")
    print("2. İyileş")
    print("3. Çık")
    
    secim = input("Seçimin (1 veya 2): ") # input ile string alıyoruz




    if secim == "1":
        player.Attack(creature) # Hedef (creature) parametre olarak gönderildi
        
        # Eğer düşman ölmediyse o da bize vursun
        if creature.hp > 0:
            creature.Attack(player)
            
    elif secim == "2":
        player.Heal()
        # İyileşirken de düşman bize vurabilir (Sıra atabanlı oyun kuralı)
        if creature.hp > 0:
            creature.Attack(player)
    elif secim == "3":
        break
    else:
        print("Geçersiz seçim, tekrar dene.")