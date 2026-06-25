a = [int(input(" enetr a number :")) for i in range(3)]
p = "the max is"
if(a[0]>a[1] and a[0]>a[2]): 
    print(p,a[0])
elif(a[1]>a[0] and a[1]>a[2]):
    print(p,a[1])
else:
    print(f"max is {a[2]}")