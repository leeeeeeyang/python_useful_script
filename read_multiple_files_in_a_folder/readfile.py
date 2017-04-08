import pandas as pd
import os
import glob



path = r'C:\Users\Leyang Cheng\Desktop\takehome\rea' 
allFiles = glob.glob(path + "/*.csv")


bby_dict = {}

for file_ in allFiles:
        df = pd.read_csv(file_)     ##read dataframe
        base = os.path.basename(file_)
        file_name = os.path.splitext(base)[0]   ##get file name without path name
        bby_dict[file_name] = df.head()

print(type(bby_dict['p1']))
