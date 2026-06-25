import pandas as pd
#calories = { "day 1" : 1200,"day 2" : 1300,"day 3" : 1500 }
#series = pd.Series(calories)
#series.loc["day 1"] += 500
#print(series[series>=1500])

data = {" name": ["pooja","kajal","aishwarya"],
        "age":[35,40,52] }
df= pd.DataFrame(data,index=["fav3","fav2","fav1"])
#new column
df["attributes"]= ["perfect waist, thighs and shape","eyes, race,smile","eyes,shape,intellect"]
#new row
new_row = pd.DataFrame({" name":"anna hathaway","age":43,"attributes":"evergreen,smile,sexy"},index=["fav4"])
df=pd.concat([df,new_row])
print(df)

