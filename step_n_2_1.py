import os

path_notebook = '/media/lofowl/My Passport/2_kaggle_notebooks'

notebooks = os.listdir(path_notebook)

notebooks = [i.split("_")[0] for i in notebooks]

unique_notebooks = set(notebooks)

with open('log_notebooks_versions.txt','w') as file:
    for notebook in unique_notebooks:
        file.write(f'{notebook} {notebooks.count(notebook)}\n')