# Wedding registry code for Wedding Butler
# created by Ben Weaver


store = input("Where would you like to register? ")
print(store)
                                  
registryList = []


while True:
    item = input("enter which items you want and how many to add them to your registry. type 'done' to finish ")
    if item not in registryList:
        registryList.append(item)
    else:
        print("item already added!")
    if item == 'done':
        del registryList[-1]
        break

print("Here is your registry at " + store + " Total items: ")
totalItems = len(registryList)
print(totalItems)
print(registryList)
