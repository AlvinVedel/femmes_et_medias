import pandas as pd
import os

def combined_df_csv(location_path):
    path = location_path
    dfs = []
    for i in range(13, 24): 
        if i not in [14, 20]:
            print(i)
            new_path = path + str(i) + ".csv"
            df = pd.read_csv(new_path, sep='\t')
            year_col = []
            annee = 20*100+i
            for j in range(0, len(df)):
                year_col.append(annee)
            df["year"] = year_col
            dfs.append(df)
            
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_csv("/home/data/ter_meduse_log/mdw_2024/data/concat/concat_all.csv")

combined_df_csv("/home/data/ter_meduse_log/mdw_2024/data/separated/data_20")


