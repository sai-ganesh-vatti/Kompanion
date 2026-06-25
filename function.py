heroes = ["ironman","superman,thor,captain america"]
chess = ["guki","arjun,prag,vishy,magi,fabi,hikaru"]
def printlen(list):
    print(len(list))
    return len(list)

def printitem(list):
    for item in list:
        print(item,end="")

printitem(chess)