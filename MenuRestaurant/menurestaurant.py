import re

class Restaurant:
    def __init__(self, name):
        self.name = name


class Menu:
    def __init__(self, Restaurant):
        self.Restaurant = Restaurant


class MenuItem:
    def __init__(self, Menu, category, meal_name, price):
        self.Menu = Menu
        self.category = category
        self.meal_name = meal_name
        self.price = price

class Order:
    def __init__(self, code):
        self.code = code


f = open ('file.txt','r')
content = f.read()
f.close()

print(content)