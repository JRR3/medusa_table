import pandas as pd 
import os

df = pd.read_csv("hash_map.csv", header=0)
print(df)
columns = df.columns.to_list()
LS0 = "END"
LS1 = "END-1"
df[LS0] = ""
df[LS1] = ""

def remove_junk(source, junk):
    useless = "@noparams"
    txt = source
    if isinstance(junk,str):
        txt = txt.replace(junk,"")
    elif isinstance(junk, list):
        for j in junk:
            txt = txt.replace(j,"")

    txt = txt.replace(useless,"")
    return txt


for idx , row in df.iterrows():

    h = row["hash"]
    sample = row["sample"]
    modality = row["modality"]
    path = row["path"]
    common = sample + "@" + modality + "@"
    nodes = path.split("/")
    ls0_node = nodes[-1]
    ls1_node = nodes[-2]

    ls0_node = remove_junk(ls0_node, common)
    ls1_node = remove_junk(ls1_node, common)

    df.loc[idx, LS0] = ls0_node
    df.loc[idx, LS1] = ls1_node

    if "|" in sample or "+" in sample:
        new_sample_name = "merge"
        df.loc[idx,"sample"] = new_sample_name

columns = columns[:-2] + [LS0, LS1] + [columns[-1]]

df = df[columns]
df.to_csv("simple_report.csv", index=False)

