def show(n):
    if n == 0:
        return
    print(n)
    show(n-1)

def sum(n):
    if n ==0:
        return 0
    return sum(n-1)+n

print(sum(5))