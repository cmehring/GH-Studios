# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 19:41:18 2019

@author: sun
"""
budget = input("enter the budget")

budget = float(budget)


if budget < 1:
    print("Invalid input")
    
else:
    print("Your wedding budget is",budget)    


name = input("input name of wedding venue")
wish = input("input the wish to marry in the church")
location = input("input location of wedding venue")
contact = input("input contact info od wedding venue")
cost = input("input cost of renting the wedding venue")

cost = float(cost)

new_budget = budget-cost

if budget > new_budget:
    print("you are under budget , you have left your budget")
else:
    print("you are over budget, you have to cut bacck on your cost")

    
print("enter info about catering")

caterer_name = input("input name of caterer")
caterer_location = input("input location of caterer")
caterer_contact = input("input contact info of wedding venue")
caterer_cost = input("input cost of hiring a caterer")
plate_n = input("input the count of plate")
caterer_cost_plate = input("input cost of each plate")

new_budget2 = new_budget-(float(caterer_cost)+int(plate_n)*float(caterer_cost_plate))

print("your updated budget is",new_budget2)

if new_budget > new_budget2:
    print("you are unber budget. you have left in your budget")
else:
    print("you are over budget, you have to cut back on your cost")
    

print("enter info about entertainment")

music = input("input ceremony music")
cocktail = input("input cocktail party music")
music_meals = input("input music with meals")
band = input("input symphony,band or disco")
type_entertainment = input("input type of entertainment")
name_entertainer = input("input name of entertainer")
contact_entertainer = input("input contact info of entertainer")
cost_entertainer = input("input cost of hiring the entertainer")


new_budget3 = new_budget2-float(cost_entertainer)

print("your updated budget is",new_budget3)

if new_budget2 > new_budget3:
    print("your are unber budget,you have left in your hand")
    
else:
    print("you are over budget. you have to cut back on your cost")

    
print("enter info about ceremony performer")
name_performer = input("input name of performer")
contact_performer = input("input contact info of entertainer")
cost_performer = input("input cost of hiring the performer")


new_budget4 = new_budget3-float(cost_performer)

print("your updated budget is",new_budget4)

if new_budget3 > new_budget4:
    print("you are unber budget you have left in your budget")
else:
    print("you are over budget you have to cut back on your cost")


print("enter info about bar")
     
type_drink = input("input type of drink") 
name_drink = input("input name of drink")   
cost_hiring_bartender = input("input cost of hiring a bartender") 
drink_n = input("the count of drink")
cost_each_drink = input("input cost of each drink") 

new_budget5 = new_budget4 - (int(drink_n)*float(cost_each_drink))
print("your updated budget is",new_budget5)

if new_budget4 > new_budget5:
    print("your are unber budget you have left in your budget")
 
else:
    print("you are over budget you have to cut back on your cost")


print("enter info about Gifts")

invitations = input("input wedding invitations")
count_gifts = input("input gifts for guests")
cost_gift = input("input cost of gift")
souvenir = input("input wedding souvenir")
other_gifts = input("input other gifts")

    
new_budget6 = new_budget5-(int(count_gifts)*float(cost_gift))
print("your updated budget is",new_budget6)

if new_budget5 > new_budget6:
   
    print("you are under budget ,you have left in your budget")
    
else:
    print("you are over budget you have to cut back on your cost")

print("enter info about flowers")

bouquet = input("input bridal bouquet")
fireworks = input("input the fireworks of the groom and the best man")
n_flower = input("the count of flower")
cost_flower = input("the cost of a flower")

new_budget7 = new_budget6 - (int(n_flower)*float(cost_flower))

print("your updated budget is",new_budget7)

if new_budget7>0:
    print("you are under budget you have left in your budget")
else:
    print("you are over budget you have to cut back on your cost")
    


print("remainder amount is",new_budget7)    
    
    
    
    
    
    
    
    
    


























    
 