import pandas as pd

error = list()
with open("kaggle_notebook_view_count_versions.csv","r") as file:
    file = file.read().split("\n")
    lines = [i.split(",") for i in file]
    with open("clean_kaggle_notebook.csv","a+") as file:
        for line in lines:
            try:
                if int(line[2]) >= 2:
                    file.write(",".join(line)+"\n")
            except Exception as e:
                error.append(line)

with open("error_kaggle_notebook.csv","a+") as file:
    for line in error:
        file.write(",".join(line)+"\n")


