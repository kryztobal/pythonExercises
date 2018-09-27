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
        self.index = 0
        self.category = category
        self.meal_name = meal_name
        self.price = price

class Order:
    def __init__(self, restaurant="", MenuItems = []):
        self.restaurant = restaurant
        self.menuItems = MenuItems
    
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

    def createOrderFile(self):
        f = open('miorder.txt', 'w')
        f.write("holaaaaaa")

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
    print(category[0].category)
    for meal in category:
        print(str(meal.index)+'.     '+meal.meal_name+'\t\t\t\t\t\t\t\t'+meal.price)

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
    print("0. Quit")
    opcion = int(input("ingrese la opcion del menu del restaurante que desee: "))
    if(opcion != 0):
        clear_console()
        
        restaurant = restaurants[opcion-1]
        print("Welcome to "+restaurant.name)
        order = Order(restaurant.name)
        
        meal_option = None
        while(meal_option != 'q' and meal_option != 'Q'):
            clear_console()
            print("NewMeal(n)                           Quit(q)")
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
                print("================================================")
                print("Your current meal has "+str(len(order.menuItems))+" item(s).")
                for meal in order.menuItems:
                    print(str(meal.index)+"\t"+meal.category+"\t\t"+meal.meal_name+"\t\t\t"+meal.price)
                print("================================================")
                print("\t\t\t\t\t\tTotal = "+str(order.getTotalOrder()))
            meal_option = input("Please enter item[1.."+str(lenIndex(menuItems))+"]: ")
            

            if(re.match('\d',meal_option)):
                if(int(meal_option) > 0 and int(meal_option) <= lenIndex(menuItems)):
                    order.addMeal(getMeal(meal_option, menuItems))
                    #print(getMeal(meal_option, menuItems).meal_name)
            elif(re.match('n|N', meal_option)):
                if(len(order.menuItems) > 0):
                    order.createOrderFile()
            elif(re.match('q|Q', meal_option)):
                    pass
            else:
                exit = input("Option no valid, press any key for continue...")