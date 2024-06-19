import pandas as pd 
import os
from collections import defaultdict

df = pd.read_csv("hash_map.csv", header=0)
print(df)
original_columns = df.columns.to_list()

LS0 = "END"
KW_dim_red = "DimRedKeyWord"
KW_norm = "NormKeyWord"
KW_tmc = "TMCKeyWord"
LS1 = "END-1"

new_columns = [LS0,KW_dim_red,KW_norm,KW_tmc,LS1]

for column in new_columns:
    df[column] = ""

dim_reduction_kw = ["umap", "tsne", "phate", "pca"]
norm_kw = ["ct_norm"]
tmc_kw = ["tree"]

list_of_keywords = dim_reduction_kw + norm_kw + tmc_kw

kw_to_cat = {}
cat_to_kw = {}

cat_to_kw[KW_dim_red] = dim_reduction_kw
for kw in dim_reduction_kw:
    kw_to_cat[kw] = KW_dim_red

cat_to_kw[KW_norm] = norm_kw
for kw in norm_kw:
    kw_to_cat[kw] = KW_norm

cat_to_kw[KW_tmc] = tmc_kw
for kw in tmc_kw:
    kw_to_cat[kw] = KW_tmc


def has_keyword(source, idx):
    visited_cat = {}
    for word in list_of_keywords:
        if word in source:
            cat = kw_to_cat[word]
            if cat not in visited_cat:
                df.loc[idx,cat] = word
                visited_cat[cat] = word
            else:
                if visited_cat[cat] == "pca":
                    df.loc[idx,cat] = word
                    visited_cat[cat] = word




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
    has_keyword(path, idx)

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

columns = original_columns[:-2]
columns += new_columns
columns += [original_columns[-1]]

df = df[columns]
df.to_csv("simple_report.csv", index=False)

