import re
# import only system from os 
from os import system, name 

class Restaurant:
    def __init__(self, name, Menu = None, orders = []):
        self.name = name
        self.Menu = Menu
        self.order = orders

class Menu:
    def __init__(self, MenuItems = []):
        self.menuItems = MenuItems

class MenuItem:
    def __init__(self, category, meal_name, price):
        self.category = category
        self.meal_name = meal_name
        self.price = price

class Order:
    def __init__(self, code):
        self.code = code


def getMenuItem(menuObjects):
        category = menuObjects[0]
        menuObjects.remove(category)

        price = menuObjects[-1]
        menuObjects.remove(price)

        meal_name = ""
        for item in menuObjects:
            meal_name += ( item+' ' )
        meal_name = meal_name.strip()

        return MenuItem(category, meal_name, price)

def clear_console(): 
    if name == 'nt': 
        _ = system('cls') 
  
    else: 
        _ = system('clear') 

def clear(content):
    contentcleaned = []
    for item in content:
        if(item != '\n'):
            contentcleaned.append(item)
    return contentcleaned

def groupByCategory(menuItems):
    menuItemsGroup = {'Appetizers':[], 'Drinks':[], 'Entrées':[], 'Deserts':[]} 
    for item in menuItems:
        menuItemsGroup[item.category].append(item)
    return menuItemsGroup

def showMeals(category, index = 1):
    print(category[0].category)
    for meal in category:
        print(str(index)+'.     '+meal.meal_name+'\t\t\t\t\t\t\t\t'+meal.price)
        index += 1
    return index

def readRestaurantFile():
    f = open ('file.txt','r')
    content = clear(f.readlines())
    f.close()
    if(len(content)>0):
        restaurants = []
        for index in range(0, len(content)):
            if(len(content) >= 2):
                menuItems = []
                patron = re.compile(' |, ')
                menuLine = patron.split(content[1])
                auxline = []
                for item in menuLine:
                    auxline.append(item)
                    if(re.search('\$', item)):
                        menuItems.append(getMenuItem(auxline))
                        auxline = []
                restaurant = Restaurant(content[0], Menu(menuItems))
                restaurants.append(restaurant)
                content.remove(content[0])
                content.remove(content[0])
            auxline = []
        return restaurants        
    else:
        print("File is empty")
        return []

restaurants = readRestaurantFile()

opcion = None

while(opcion != 0):
    clear_console()
    for index in range(0,len(restaurants)):
        print(str((index+1))+". "+restaurants[index].name)
    print("0. Quit")
    opcion = int(input("ingrese la opcion del menu del restaurante que desee: "))
    if(opcion != 0):
        meal_option = None
        while(meal_option != 'q'):
            clear_console()
            restaurant = restaurants[opcion-1]
            print("Welcome to "+restaurant.name)
            print("NewMeal(n)                           Quit(q)")
            menuItems = groupByCategory(restaurant.Menu.menuItems)

            appetizers = menuItems['Appetizers']
            drinks = menuItems['Drinks']
            entrees = menuItems['Entrées']
            deserts = menuItems['Deserts']

            if(len(appetizers) > 0):
                index = showMeals(appetizers)
            if(len(drinks) > 0):
                index = showMeals(drinks, index)
            if(len(entrees) > 0):
                index =showMeals(entrees, index)
            if(len(deserts) > 0):
                index = showMeals(deserts, index)
            meal_option = input("Please enter item[1.."+str((index-1))+"]: ")
            print(meal_option)
            test = input()