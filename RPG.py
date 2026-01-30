import random as rnd
import Magaza

class Character:
    def __init__(self, name="none"): # Varsayılan isim atadık
        self.hp = 100
        self.ad = rnd.randint(5, 15) # Hasarı biraz artırdım
        self.name = name
        self.xp = 0
        self.level = 1
        self.xp_to_nextlevel = 20

        # Envanter

        self.potion = 10

    def xpGained(self,target):
        self.xp += target.xp
        if(self.xp >= self.xp_to_nextlevel):
            self.level += 1
            print("LEVEL ATLADIN.")
            self.ad += rnd.randint(5,10)
            print(f"YENİ SALDIRI HASARIN: {self.ad}")
            print(f"Yeni Level: {self.level}")
            self.xp -= self.xp_to_nextlevel
            self.xp_to_nextlevel += 10
        else:
            pass
    

    
    def Info(self):
        print(f"[{self.name}] Can: {self.hp} | Güç: {self.ad} | Level: {self.level} | XP:{self.xp}")




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
        if(self.potion > 0):
            if(self.hp==100):
                print("Canın zaten dolu")
            else:
                self.hp += 15 # Değer ataması düzeltildi (+=)
                if(self.hp >= 100):
                    self.hp = 100
                self.potion -= 1        
                print(f"💚 {self.name} iyileşti. Yeni Can: {self.hp}. Kalan iksir:{self.potion}")
        else:
            print("İksirin kalmadı!!!")

class Enemy(Character):
    def __init__(self):
        # Önce rastgele bir ırk seçelim
        races = ["Goblin", "Ork", "Blight", "Troll"]
        race_name = rnd.choice(races)

       
        
        # ŞİMDİ üst sınıfın (Character) özelliklerini çağırıyoruz
        # super().__init__(name) diyerek ismi yukarıya gönderiyoruz
        super().__init__(name=race_name)

        if(self.name == "Ork"):
            self.xp = 25
        elif(self.name == "Troll"):
            self.xp = 20
        elif(self.name == "Goblin"):
            self.xp = 10
        else:
            self.xp = 15
        
        # Düşmanın canını kahramandan biraz daha az yapabiliriz (isteğe bağlı)
        self.hp = rnd.randint(20,30)
        self.ad = 5

    # Attack ve Info metodların aynen kalabilir...
    def Attack(self, target):
        damage = self.ad
        target.hp -= damage
        print(f"👹 {self.name} sana saldırdı! {damage} hasar aldın.")
        
# --- OYUN BAŞLIYOR ---

isim = input("Kahramanın adı ne olsun?: ")
player = Hero(isim)
creature = Enemy()



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
        player.xpGained(creature)
        creature = Enemy()
        Magaza.Magaza(player)
        print(f"\nKarşına vahşi bir {creature.name} çıktı!")
        


    print("\nNe yapacaksın?")
    print("1. Saldır")
    print("2. İyileş")
    print("3. Çık")
    
    secim = input("Seçimin : ") # input ile string alıyoruz




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