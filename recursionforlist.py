def listshow(list,idx):
    if(idx==len(list)):
        return
    print(list[idx],end="")
    listshow(list,idx+1)

ff = ["alok","","k","","kelly","","hayato"]
listshow(ff,0)