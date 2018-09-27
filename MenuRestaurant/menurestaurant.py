import re
import uuid
import time
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
        self.index = 0
        self.category = category
        self.meal_name = meal_name
        self.price = price

class Order:
    def __init__(self, restaurant="", MenuItems = [], tip = None):
        self.restaurant = restaurant
        self.menuItems = MenuItems
        self.tip = tip
    
    def setOrder(self, MenuItems):
        self.menuItems = MenuItems

    def addMeal(self, meal):
        self.menuItems.append(meal)
    
    def getTotalOrder(self):
        total = 0
        for meal in self.menuItems:
            patron = re.compile('\$')
            total += float(patron.sub('',meal.price))
        return total   
    
    def setTip(self, tip):
        self.tip = tip

    def createOrderFile(self, tip):
        uid = uuid.uuid4()
        patron = re.compile('-')
        code = patron.split(str(uid))[0]

        patron = re.compile('\n')
        restaurant = patron.sub('', self.restaurant)
        f = open("order_"+code+'_'+restaurant+'_'+time.strftime("%d%m%Y")+'_'+time.strftime("%H%M%S")+'.txt', 'w')
        f.write(self.restaurant)
        f.write("Date: "+time.strftime("%d/%m/%Y")+'\n')
        f.write("\n=========================================================")
        for meal in self.menuItems:
            f.write("\n"+meal.category.ljust(20)+meal.meal_name.ljust(30)+meal.price.ljust(50))
        f.write("\n=========================================================")
        subtotal = self.getTotalOrder()
        tax = round(subtotal * 0.07, 2)
            
        total = subtotal + tax + float(tip)
        f.write("\n\nSubTotal".ljust(11)+"= $"+str(subtotal))
        f.write("\nTax".ljust(11)+"= $"+str(tax))
        f.write("\nTip".ljust(11)+"= $"+str(tip))
        f.write("\nTotal".ljust(11)+"= $"+str(total))
        f.close()


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
    
    index = 1

    for item in menuItemsGroup['Appetizers']:
        item.index = index
        index += 1
    
    for item in menuItemsGroup['Drinks']:
        item.index = index
        index += 1
    
    for item in menuItemsGroup['Entrées']:
        item.index = index
        index += 1

    for item in menuItemsGroup['Deserts']:
        item.index = index
        index += 1

    return menuItemsGroup

def showMeals(category):
    print('\n')
    print("---------------------------------------------------------------------")
    print(category[0].category.upper())
    print("---------------------------------------------------------------------")
    for meal in category:
        print(str(meal.index).ljust(5)+meal.meal_name.ljust(50)+meal.price.ljust(30))

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

def lenIndex(menuItems):
    return len(menuItems['Appetizers']) + len(menuItems['Drinks']) + len(menuItems['Entrées'])+ len(menuItems['Deserts'])

def getMeal(index, menuItems):
    for item in menuItems['Appetizers']:
        if(item.index == int(index)):
            return item
    
    for item in menuItems['Drinks']:
        if(item.index == int(index)):
            return item
    
    for item in menuItems['Entrées']:
        if(item.index == int(index)):
            return item

    for item in menuItems['Deserts']:
        if(item.index == int(index)):
            return item

restaurants = readRestaurantFile()

opcion = None

while(opcion != 0):
    clear_console()
    for index in range(0,len(restaurants)):
        print(str((index+1))+". "+restaurants[index].name)
    print("0. Quit\n")
    opcion = int(input("Please enter to option: "))
    if(opcion != 0):
        clear_console()
        restaurant = restaurants[opcion-1]
        order = Order(restaurant.name)
        meal_option = None
        key = False
        while(meal_option != 'q' and meal_option != 'Q'):
            clear_console()
            print("WELCOME TO "+restaurant.name)
            print("NewMeal(n)                           Quit(q)".rjust(58))
            menuItems = groupByCategory(restaurant.Menu.menuItems)

            appetizers = menuItems['Appetizers']
            drinks = menuItems['Drinks']
            entrees = menuItems['Entrées']
            deserts = menuItems['Deserts']

            if(len(appetizers) > 0):
               showMeals(appetizers)
            if(len(drinks) > 0):
               showMeals(drinks)
            if(len(entrees) > 0):
               showMeals(entrees)
            if(len(deserts) > 0):
               showMeals(deserts)

            if(len(order.menuItems) > 0):
                print("\n=====================================================================")
                print("Your current meal has "+str(len(order.menuItems))+" item(s).")
                for meal in order.menuItems:
                    print(str(meal.index).ljust(5)+meal.category.ljust(20)+meal.meal_name.ljust(30)+meal.price.ljust(50))
                print("=====================================================================")
                subtotal = order.getTotalOrder()
                tax = round(subtotal * 0.07, 2)
                print("SubTotal = $".rjust(56)+str(subtotal))
                print("Tax = $".rjust(56)+str(tax))
                total = 0
                if(order.tip != None):
                    total += float(order.tip) 
                    print("Tip = $".rjust(56)+str(order.tip))
                total = subtotal + tax 
                print("Total = $".rjust(56)+str(total))
            if(key):
                key = False
                print("\nYour ticket has create!!")

            meal_option = input("\nOptions: \n [1.."+str(lenIndex(menuItems))+"]: Add meals to order \n [q]: Quit \n [n]: Generate order \n\nPlease enter item: ")

            if(re.match('\d',meal_option)):
                if(int(meal_option) > 0 and int(meal_option) <= lenIndex(menuItems)):
                    order.addMeal(getMeal(meal_option, menuItems))
            elif(re.match('n|N', meal_option)):
                tip = None
                while(True):
                    tip = input("Please enter TIP: ")
                    if(re.match('\d',tip)):
                        order.setTip(tip)
                        break
                    else:
                        print('Tip invalid')
                if(len(order.menuItems) > 0):
                    order.createOrderFile(tip)
                    key = True
                else:
                    exit = input("You don't has select any meal, press any key for continue...")
            elif(re.match('q|Q', meal_option)):
                    pass
            else:
                exit = input("Option no valid, press any key for continue...")