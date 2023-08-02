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

SOURCE_DIR = "ISicily-ISicily-cf52385/inscriptions"
TARGET_DIR = "output_csv"

# clean target dir by deleting and recreating
shutil.rmtree(TARGET_DIR, ignore_errors=True)
os.mkdir(TARGET_DIR)

docs = []

# get all files in source dir
for file in tqdm.tqdm(glob.glob(f"{SOURCE_DIR}/*.xml")):
    with open(file) as f:
        doc = epidoc.load(f)
    docs.append(doc)
    # break

output_docs = []


# Get Title, All instances of idno and terms
# Terms hide under textClass

for doc in tqdm.tqdm(docs):
    line = {}
    line["title"] = doc.title
    line["idno"] = doc.idno
    line["terms"] = doc.terms
    output_docs.append(line)

# Write to CSV
with open(f"{TARGET_DIR}/output.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "idno", "terms"])
    writer.writeheader()
    for doc in output_docs:
        writer.writerow(doc)



