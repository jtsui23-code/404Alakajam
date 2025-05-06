import pygame

class Item:
    def __init__(self, name, description, price, quantity, coins):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.coins = 0

    def __str__(self):
        return f"Item(name={self.name}, description={self.description}, price={self.price}, quantity={self.quantity})"
    
    def addCoins(self, coinAmount):
        self.coins = coinAmount

    