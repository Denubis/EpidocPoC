#!/usr/bin/env python3
# Epidoc to csv converter
# Brian Ballsun-Stanton
# MIT License

import glob
import csv
import epidoc
import shutil
import os
import tqdm
import json
import numpy as np
import pandas as pd

SOURCE_DIR = "ISicily-ISicily-cf52385/inscriptions"
TARGET_DIR = "output"

# clean target dir by deleting and recreating
shutil.rmtree(TARGET_DIR, ignore_errors=True)
os.mkdir(TARGET_DIR)

docs = []

# get all files in source dir
for i, file in enumerate(tqdm.tqdm(glob.glob(f"{SOURCE_DIR}/*.xml"))):
    with open(file) as f:
        doc = epidoc.load(f)
    docs.append(doc)
    # if i > 10:
    #     break
    # break

output_docs = []


# Get Title, All instances of idno and terms
# Terms hide under textClass

max_terms = 0

for doc in tqdm.tqdm(docs):
    line = {}
    line["title"] = doc.title
    line["idno"] = doc.idno
    for i, term in enumerate(doc.terms):
        # prepend _{i} to each key inside term
        for key in term.copy().keys():
            term[f"term_{key}_{i}"] = term.pop(key) 
        line[f"term_{i}"] = term
        if max_terms < i:
            max_terms = i

    output_docs.append(line)



# Write to JSON
with open(f"{TARGET_DIR}/output.json", "w") as f:
    json.dump(output_docs, f, indent=4)



# Make output_docs a dataframe
df = pd.DataFrame(output_docs)
# flatten the idno dictionary into the dataframe
df = pd.concat([df.drop(["idno"], axis=1), df["idno"].apply(pd.Series)], axis=1)
for i in range(max_terms+1):
    print(i)
    df = pd.concat([df.drop([f"term_{i}"], axis=1), df[f"term_{i}"].apply(pd.Series)], axis=1)

# Write to CSV
df.to_csv(f"{TARGET_DIR}/output.csv", index=False)


