

final = list()
with open("clean_kaggle_notebook.csv","r") as file:
    file = file.read().split("\n")
    final += [i.split(",") for i in file]

with open("error_kaggle_notebook_recollect.csv","r") as file:
    file = file.read().split("\n")
    final += [i.split(",") for i in file]

with open("final_kaggle_notebook.csv","a+") as file:
    for line in final:
        try:
            if int(line[2]) >= 2:
                file.write(",".join(line)+"\n")
        except:
            pass