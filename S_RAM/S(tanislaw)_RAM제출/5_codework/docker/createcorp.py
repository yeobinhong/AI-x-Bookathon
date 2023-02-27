import os
import pandas as pd

buf = []
for i in os.listdir('res'):
    df = pd.read_csv("res/"+i)
    for j in range(1,len(df)):
        if pd.isna(df.iloc[j][-1]):
            continue
        buf.append(df.iloc[j][-1])
df = pd.DataFrame(buf,columns=['context'])
df.to_csv('corp.csv')