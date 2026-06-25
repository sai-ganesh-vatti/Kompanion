def check(n):
    if n>=0:
        if n%2 == 0:
            print(n,"is even")
        else: 
            print(n,"is odd")
    else:
        print("number is negative")

check(7)
check(-8)