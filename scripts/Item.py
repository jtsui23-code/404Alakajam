import pygame

class Item:
    def __init__(self, name, description, price, quantity, coins):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.coins = coins
        self.hpPotionAmount = 0
        self.freezePotionAmount = 0
        self.smokeBombAmount = 0
        self.weaponStrength = 1

    def __str__(self):
        return f"Item(name={self.name}, description={self.description}, price={self.price}, quantity={self.quantity})"
    
    def getCoins(self, coinAmount):
        self.coins += coinAmount

    def strengthenWeapon(self, weaponStrength):
        if self.weaponStrength < 10:
            self.weaponStrength += 1

    def addhpPotion(self, itemAmount, hpPotionAmount):
        if hpPotionAmount > 0 and itemAmount < 4:
            self.hpPotionAmount += 1
        
    def addfreezePotion(self, itemAmount, freezePotionAmount):
        if freezePotionAmount > 0 and itemAmount < 4:
            self.freezePotionAmount += 1

    def addsmokeBomb(self, itemAmount, smokeBombAmount):
        if smokeBombAmount > 0 and itemAmount < 4:
            self.smokeBombAmount += 1

    def addthornWhip(self, itemAmount, thornWhipAmount):
        if thornWhipAmount > 0 and itemAmount < 4:
            self.thornWhipAmount += 1

class hpPotion:
    def __init__(self, health, maxHealth):
        self.health = health
        self.hpPotionAmount = 0
        self.hpPotionPrice = 10
        self.maxHealth = maxHealth
    
    def __str__(self):
        return f"hpPotion(health={self.health}, hpPotionAmount={self.hpPotionAmount}, hpPotionPrice={self.hpPotionPrice})"

    def buy(self, coins):
        if coins >= self.hpPotionPrice:
            self.hpPotionAmount += 1
            coins -= self.hpPotionPrice
        else:
            print("Not enough coins to buy hpPotion.")
        return coins
    
    def useHeal(self, playerHealth, maxHealth):
        if(self.hpPotionAmount > 0 and self.health < maxHealth):
            self.health += 1
            self.hpPotionAmount -= 1

class freezePotion:
    def __init__(self, freezePotionAmount):
        self.freezePotionAmount = freezePotionAmount
        self.freezePotionPrice = 10

    def __str__(self):
        return f"freezePotion(freezePotionAmount={self.freezePotionAmount}, freezePotionPrice={self.freezePotionPrice})"

    def buy(self, coins):
        if coins >= self.freezePotionPrice:
            self.freezePotionAmount += 1
            coins -= self.freezePotionPrice
        else:
            print("Not enough coins to buy freezePotion.")
        return coins
    
    def useFreeze(self, enemy):
        if self.freezePotionAmount > 0:
            ## Battle script needs to have freeze
            ## enemy.freeze()
            self.freezePotionAmount -= 1
        else:
            print("No freeze potions left to use.")
    
class smokeBomb:
    def __init__(self, smokeBombAmount):
        self.smokeBombAmount = smokeBombAmount
        self.smokeBombPrice = 10

    def __str__(self):
        return f"smokeBomb(smokeBombAmount={self.smokeBombAmount}, smokeBombPrice={self.smokeBombPrice})"

    def buy(self, coins):
        if coins >= self.smokeBombPrice:
            self.smokeBombAmount += 1
            coins -= self.smokeBombPrice
        else:
            print("Not enough coins to buy smokeBomb.")
        return coins
    
    def useSmoke(self, enemy):
        if self.smokeBombAmount > 0:
            ## Battle script needs to have flee
            ## enemy.flee()
            self.smokeBombAmount -= 1
        else:
            print("No smoke bombs left to use.")

class thornWhip:
    def __init__(self, thornWhipAmount):
        self.thornWhipAmount = thornWhipAmount
        self.thornWhipPrice = 10

    def __str__(self):
        return f"thornWhip(thornWhipAmount={self.thornWhipAmount}, thornWhipPrice={self.thornWhipPrice})"

    def buy(self, coins):
        if coins >= self.thornWhipPrice:
            self.thornWhipAmount += 1
            coins -= self.thornWhipPrice
        else:
            print("Not enough coins to buy thornWhip.")
        return coins
    
    def useThorn(self, enemy):
        if self.thornWhipAmount > 0:
            ## Battle script needs to have thorn whip
            ## enemy.thornWhip()
            self.thornWhipAmount -= 1
        else:
            print("No thorn whips left to use.")