ListA = [1, 2, 1, 4, 7, 9, 3, 4, 2]

for i,o1 in enumerate(ListA):
    for o2 in ListA[i+1:]:
#        print(i, o1, o2)
        if o1 == o2 :
            print("Collision", i, o1, o2)
