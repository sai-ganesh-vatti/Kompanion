movies=[]
a= input("enter your 1st fav movie")
b= input("enter your 2nd fav movie")
c= input("enter your 3rd fav movie")
movies.append(a)
movies.append(b)
movies.append(c)
copy=movies.copy()
copy.reverse()
if(copy==movies):
    print("palindrome")
else:
    print("not a palindrome")