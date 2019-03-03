# 
# Copyright (c) 2019 Aditya Mitra
# Create a list and check how we can detect
# same values in list
ListA = [1, 2, 1, 4, 7, 9, 3, 4, 2, 6]
counter = 0
for i,o1 in enumerate(ListA):
    for o2 in ListA[i+1:]:
        counter += 1
        #print(i, o1, o2)
        #if o1 == o2 :
            #print("Collision", i, o1, o2)
print(counter)
