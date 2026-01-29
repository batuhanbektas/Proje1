import random as rnd

class Hero:
    def __init__(self,name=None):
        self.hp= rnd.randint(1,20)
        self.ad = rnd.randint(1,10)
        self.name = name

    def attack(self,target):
        print(target.hp)
        dice = rnd.randint(1,20)
        print(dice)
        if(dice<5):
            print("Failed")
        elif(dice==20):
            print("Critical hit")
            target.hp = target.hp - (2*self.ad)
        else:
            target.hp = target.hp - self.ad
        print(target.hp)

    def Info(self):
        print(f"""
---------Character--------
Name = {self.name}
Attack Damage={self.ad}
Health = {self.hp}
              """)
    
class Enemy:
    def __init__(self):
        self.hp = rnd.randint(1,10)
        self.ad = rnd.randint(1,5)
        races=["Goblin","Ork","Blight"]
        self.name = rnd.choice(races)
    
    def Info(self):
        print(f"""
---------Creature--------
Name = {self.name}
Attack Damage={self.ad}
Health = {self.hp}
              """)

player = Hero()
creature = Enemy()

player.Info()
creature.Info()

