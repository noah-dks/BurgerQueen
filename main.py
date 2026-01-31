import sqlite3
from colorama import Fore, Back, Style, init
from argon2 import PasswordHasher
init(autoreset=True)

ph = PasswordHasher()
con = sqlite3.connect("BQv2.db")
cursor = con.cursor()
cursor.execute("SELECT * FROM sqlite_master")


def logIn():  #used for flow and getting data from user. Checking of credentials is in a different function
   while True:
         username = input( Fore.LIGHTBLUE_EX + "\nUsername:\n" + Style.RESET_ALL)
         password = input(Fore.LIGHTCYAN_EX + "Password:\n" + Style.RESET_ALL)
         
         try:
            isEmployee = checkCreds(username, password) 
            if isEmployee is not None: #checks if user is either 0 or 1, important for following function
               separateUser(isEmployee, username)
               break
            else:
               print("Invalid password. Please try again.") #used print instead of raise because continue doesnt work with raise
               continue

         except ValueError as error: #saves the description of an error thats inside of raise in a variable called error
            answer = input(error).lower()
            if answer == "Y" or answer == "y":
               registerUser()
               break
            else:
               return

def checkCreds(username,password): #used to check whether username and passwords match, or whether the user actually exists
   cursor.execute("SELECT password, employee FROM users WHERE username = ?", (username,))
   user = cursor.fetchone()
   if user:
      storedHash, isEmployee = user #storedhash is password FROM the database - verify checks password from DB with the input password from python
      try:
         ph.verify(storedHash, password)
         return isEmployee
      except Exception:
         return None
   else:
      raise ValueError("\nCouldn’t find an account with those credentials. Create one? Y/N\n")
   

def registerUser(): 
   while True:
      try:
         isEmployee = 0  #automatically forces user to be a customer, all employees are added using sql script for safety reasons
         username = input(Fore.BLUE + "\nEnter a username:\n" + Style.RESET_ALL)
         cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
         if cursor.fetchone():
            print("That username already exists. Please choose another.")
            continue

         if not username.strip(): #strip removes spaces, so itll check if user cannot be stripped aka if user is empty
            raise ValueError(Back.BLACK + Fore.RED + "Username cannot be empty." + Style.RESET_ALL)
         elif not username.isalnum(): #checks if there are any special characters in username. alnum is alphanumeric
            raise ValueError(Back.BLACK + Fore.RED + "Username cannot have special characters." + Style.RESET_ALL)
         
         password = input(Fore.CYAN + "\nCreate a password: " + Fore.YELLOW + "\n!Minimum 6 characters\n" + Style.RESET_ALL)
         safePassword = input(Fore.GREEN + "Re-enter your password:\n" + Style.RESET_ALL)
         checkPassLength(safePassword)
         checkPassMatch(password, safePassword)
         
         hPassword = ph.hash(password)
         
         cursor.execute("INSERT INTO users (username, password, employee) VALUES (?, ?, ?)", (username, hPassword, isEmployee))
         con.commit()
         separateUser(isEmployee, username)
         return

         
      except (ValueError, TypeError) as error:
            print(error)
            continue
      
def checkPassLength(safePassword): #added a couple of restrictions; like for example, having the password be 6 or longer.
   if len(safePassword) <6:
      raise ValueError(Back.BLACK + Fore.RED + "Password needs to be longer than 6 characters\n" + Style.RESET_ALL)
   else: 
      return
   
def checkPassMatch(password, safePassword): #checks if re-entered password is the same as the original
   if safePassword != password:
      raise ValueError(Back.BLACK + Fore.RED +"Passwords do not match. Please try again" + Style.RESET_ALL)
   
   
# SEPARATION OF PROGRAM
def separateUser(isEmployee, username): #now splits system in 2, employees get different options from customers
   if isEmployee == 0:
      customerMain(username)
   elif isEmployee == 1:
      employeeMain(username)
   else: 
      print("idk what you are")

# CUSTOMER MAIN
def customerMain(username): #home as in home page, kind of a menu 
   while True:
      try:
         print("\nWhat would you like to do, " + Style.BRIGHT + username + Style.RESET_ALL + "?")
         choice = input(Fore.GREEN + "[1] " +  Style.RESET_ALL + "Order | " + Fore.YELLOW + "[2] " +  Style.RESET_ALL + "See orders | " + Fore.RED + "[3] " +  Style.RESET_ALL + "Log out\n")
         if choice == "1":
            orderBurger(username)
         elif choice == "2":
            myOrders(username)
         elif choice == "3":
            main()
         else:
            raise ValueError("Invalid option. Please choose from the options above.")
      except (ValueError, TypeError) as error:
               print(error)
               continue
      
# CUSTOMER - MAKE ORDER
#this is where user can actually make an order, this function saves data in variables which are then sent over to makeOrder.
def orderBurger(username): #this handles interaction with the user - a smaller function/ make order handles actually sending the data to the DB
   while True:
      cursor.execute("SELECT burgName FROM burgers")
      burgerRows = cursor.fetchall()
      burgerTypes = []
      for item in burgerRows: #i do this to turn the tuple list into a normal list 
         burgerTypes.append(item[0]) 

      print("\nCurrent Items on the " + Fore.RED + Style.BRIGHT + "[" + Fore.YELLOW + "Menu" + Fore.RED + "]" + Style.RESET_ALL + ":\n" + "\n".join("- 🍽️   " + item + " -" for item in burgerTypes))
      userOrder = input("\nWhat is your order? Please order one thing at a time: \n").lower()

      if userOrder in ["whopper queen", "triple cheesy princess", "kingdom fries"]:
         makeOrder(username, userOrder)
         break
      else:
         raise ValueError("\nThis isnt on the menu. Please order something else.") 
      
      
def makeOrder(username, userOrder): #this function sends checked data into the DB.
   while True:
      print( Back.BLACK + Fore.YELLOW + "\nOrder is in the making!" + Style.RESET_ALL )
      isProduced = 0 #IMPORTANT! defines order as unmade so it cant be sent over for employees later
      cursor.execute("INSERT INTO orders (clientID, productID, produced) VALUES (?, ?, ?)", (username, userOrder, isProduced))
      con.commit()

      newOrder = input("\nWould you like to order anything else? " + Back.BLACK + Fore.GREEN + Style.BRIGHT + "[Y]" + Fore.WHITE  +  " or " + Fore.RED + "[N]" + Style.RESET_ALL + "\n").lower() 
      if newOrder == "y":
         orderBurger(username)
      elif newOrder == "n":
         customerMain(username)
      else:
         raise ValueError("Invalid option. Please choose either " + Fore.GREEN + "[Y]" + Style.RESET_ALL+ " or " + Fore.RED + "[N]" + Style.RESET_ALL)

# CUSTOMER - SEE ORDERS
#Customer can see all the orders based on their own username. cant see other peoples orders. filtered by username in sql.
def myOrders(username):

   cursor.execute("SELECT orderID, productID, produced FROM orders WHERE clientID = ?", (username,))
   ordersTup = cursor.fetchall()
   if ordersTup:
      formatOrder = []
      for orderID, productID, isProduced in ordersTup: # had trouble understanding this, but this stores all pieces of info into different variables. 
         productID = productID.title() #turns lowercase burgernames into tiles: whopper queen = Whopper Queen. for aesthetic purposes.
         addExtraZeroes(orderID)

         if isProduced == 1:
            status =  Back.GREEN + Style.BRIGHT + "Ready" + Style.RESET_ALL
         else:
            status = Back.YELLOW + Fore.BLACK + "In Progress" + Style.RESET_ALL
         formatOrder.append("\nOrder #" + extraZeros + str(orderID) + ": " + productID + " | " + status)

      orders = "\n".join(formatOrder)
      print(orders)

#Main menu for employees, acts like a little sub-main for employees. 
def employeeMain(username):
   while True:
      print("\nYou are an employee, " + username)
      choice = input(Fore.GREEN + "[1] " + Style.RESET_ALL + "View Orders | " + Fore.YELLOW + "[2] " + Style.RESET_ALL 
      + "Manage orders | " + Fore.MAGENTA + "[3] " + Style.RESET_ALL + "Check Storage | " + Fore.RED + "[4] " + Style.RESET_ALL + "Log out\n")
      if choice == "1":
         allOrders(username)
      elif choice == "2":
         makeBurger(username)      
      elif choice == "3":
         checkStorage()
      elif choice == "4":
         main() 
      
#this is just for aesthetic to copy mcdonalds and their 39xx orders. Adds extra zeroes based on the length of order. Example:
# If orderID is single digit, like 7, the order WITH zeroes will be 0007. However if orderID is 32, the order WITH zeroes will be 0032. 
#order digit shall ALWAYS be 4 (due to width = 4)
def addExtraZeroes(orderID, width=4):
   global extraZeros
   stringID = str(orderID)
   extraZeros = "0" * (width - len(stringID)) #looks at how long orderID is (single digit, double digit) and subtracts that number from width (4), which leaves the perfect amount of zeroes
   return extraZeros

#Function is responsible for changing status from "in progress" to "ready" based on isProduced, also responsible for showing every order in a formatted way 
def allOrders(username):
   while True:
      cursor.execute("SELECT orderID, clientID, productID, produced FROM orders")
      employeeRows = cursor.fetchall()
      formatOrder = []
         
      for orderID, clientID, productID, isProduced in employeeRows: # had trouble understanding this, but this stores all pieces of info into different variables. 
         productID = productID.title() #turns lowercase burgernames into tiles: whopper queen = Whopper Queen. for aesthetic purposes.
         if isProduced == 1:
            status =  Back.GREEN + Style.BRIGHT + "Ready for Pickup" + Style.RESET_ALL
         else:
            status = Back.YELLOW + Fore.BLACK + "In Progress" + Style.RESET_ALL
      
         addExtraZeroes(orderID)
         formatOrder.append(Fore.RED + "\n#" + extraZeros  + str(orderID) + Style.RESET_ALL + Style.BRIGHT + " | "  + Style.RESET_ALL + clientID + ": " + productID + Style.BRIGHT + " | " + Style.RESET_ALL + status)
         
      print("\n".join(formatOrder))
      orderFeedback(employeeRows)  

      inputIfModify = input("\nWould you like to do something with the orders? (ONE at a time!) Y/N\n").lower()
      if inputIfModify == "y":
         makeBurger(username)
      elif inputIfModify == "n":
         employeeMain(username)


#Checks what feedback to give user - if list is empty (aka there are no orders) or whether all orders are alreadt made - and there are no orders employee can make
def orderFeedback(employeeRows):
   if len(employeeRows) == 0: 
      print("No more orders left to make!")

   #iterates through each order made and checks produced, if produced amount is the same as length of a list, it means all orders are ready
   producedCount = 0
   for row in employeeRows:
      if row[3] == 1:
            producedCount += 1
   if producedCount == len(employeeRows):
      print(Back.BLACK + Fore.YELLOW +"\nAll orders finished and ready for pick up!" +  Style.RESET_ALL)


#function that actually marks burger as ready and changed produced from 0 to 1. If unmade order with matching ID to the input is found, it marks the order as produced
def makeBurger(username):
   while True:
      cursor.execute("SELECT orderID, productID, produced FROM orders")
      orderRow = cursor.fetchall()
      keyIDWithZero = input("Which order would you like to make? (ONE at a time!) \n") 

      keyIDNoZero = keyIDWithZero.replace(extraZeros, "") #makes it possible to write both 000x and x. Cancels out the functionality of extraZeros

      found = False

      try:
         for orderID, productID, isProduced in orderRow: 
            if str(orderID) == keyIDNoZero:
               if isProduced != 1:
                  isProduced = 1
                  productID = productID.title()
                  status =  Back.GREEN + Style.BRIGHT + "Ready for Pickup" + Style.RESET_ALL
                  subtractIngredients(productID)

                  cursor.execute("UPDATE orders SET produced = ? WHERE orderID = ?", (isProduced, orderID))
                  con.commit()

                  addExtraZeroes(orderID)
                  print("Order: #" + extraZeros + str(orderID) + " " + productID + " | Status: " + status)
                  found = True
                  employeeMain(username)
                  return
               else:
                  raise ValueError("That order is already marked as ready.")
               
         if not found:
            raise ValueError(Back.BLACK + Fore.RED +"Cant find an unmade order with that ID." + Style.RESET_ALL)
         
      except (ValueError) as error:
         print(error)
         employeeMain(username)


#makes a storage variable which is used as a "virtual" quantity of ingredients - subtract ingredients based on what burger uses which ingredients.
#that is found using burgeriD and product. product variable is what user has ordered - meaning its a saved type of burger from previous functions
#then i use product to find a burger ID, and using burgerID i find all ingredients which said burger uses

def subtractIngredients(productID):
   #first paragraph gets burgerID based on the product made in makeOrder.
   cursor.execute("SELECT burgerID FROM burgers WHERE burgName = ?", (productID,))
   burgerRow = cursor.fetchone()
   if burgerRow is None:
      raise ValueError("Burger " + productID + " not found in burgers table")
   burgerID = burgerRow[0]

   #uses burgerID to get ingredients which the burger uses
   cursor.execute("SELECT ingredients FROM burgIngredients WHERE burgerID = ?", (burgerID,)) 
   ingredientInBurger = cursor.fetchall()

   for (ingredID,) in ingredientInBurger: #its still a tuple so the comma after ingredID is necessary 
      cursor.execute("SELECT quantityStorage FROM ingredients WHERE ingredID = ?", (ingredID,))
      row = cursor.fetchone()
      storage = row[0]
      if storage <= 0:
         raise ValueError("Ingredient " + str(ingredID) + " is out of stock")
      else:
         storage -= 1

      cursor.execute("UPDATE ingredients SET quantityStorage = ? WHERE ingredID = ?", (storage, ingredID))
   con.commit()


#this function checks storage based on what ingredient employee wants to check - uses data from ingredients and match case to check which storage to open
def checkStorage():
   cursor.execute("SELECT ingredID, ingredName, quantityStorage FROM ingredients")
   ingredientRow = cursor.fetchall()
   ingredientType =  []

   for ingredID, ingredName, quantityStorage in ingredientRow:
      ingredientType.append("\n#" + str(ingredID) + " | "  + "Ingredient: " + ingredName + " | "  + "In Stock: " + str(quantityStorage)) #the base for storage, now match case will replace ingredID with what user wants to check

   ingredientTypeInput = input("\nWhich ingredient would you like to check?\n[1] Burger Bread\n[2] Burger Patty\n[3] Cheese\n[4] Lettuce\n[5] Tomato\n[6] Pickle\n[7] Potato\n[8] Everything\n")
   match ingredientTypeInput:
      case "1":
         print(ingredientType[0])
      case "2":
         print(ingredientType[1])
      case "3":
        print(ingredientType[2])
      case "4":
        print(ingredientType[3])
      case "5":
         print(ingredientType[4])
      case "6":
         print(ingredientType[5])
      case "7":
         print(ingredientType[6])
      case "8":
         for item in ingredientType:
            print(item)

#The intro-function starting the entire program. Here user can choose whether they want to log in, register, or exit, and the rest is taken further by following functions
def main():
    while True:
      try:
         userinput = input("-" * 4 + Fore.YELLOW + " Burger " + Fore.RED + "Queen " + Style.RESET_ALL + "-" * 4 + 
         "\nWhat would you like to do?\n"  + Fore.GREEN +  "[1] " + Style.RESET_ALL + "Log in" + Fore.YELLOW + "\n[2] " 
         + Style.RESET_ALL + "Sign up" + Fore.RED  + "\n[3] " + Style.RESET_ALL + "Log Out | Exit\n").lower()
         
         if userinput == "1":
            logIn()
         elif userinput == "2":
            registerUser()
         elif userinput == "3":
            con.close()
            exit()
         else: 
            raise ValueError("Invalid option, please try again\n")
      except (ValueError, TypeError) as error:
            print(error)
            continue
      
if __name__ == "__main__":
   main()
