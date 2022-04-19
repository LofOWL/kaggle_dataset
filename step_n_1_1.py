import pandas as pd
from tqdm import tqdm
kernel_versions = pd.read_csv('./meta_data/KernelVersions.csv')

# filter out the notebooks
#with open("url_kaggle_notebook.csv","r") as file:
#    file = file.read().split("\n")[:-1]
#    containers = [i.split(" ") for i in file]
#    notebooks = [i for i in containers if i[2] in ['8','9']]

kernels_notebooks = pd.read_csv('Filter_Kernels_Url_Notebooks.csv')

versions_id = kernel_versions['ScriptId']

notebooks_dict = {int(i):0 for i in list(kernels_notebooks['Id'])}

for id in tqdm(versions_id):
    if id in notebooks_dict.keys():
        notebooks_dict[id] = notebooks_dict[id] + 1

counts = notebooks_dict.values()

kernels_notebooks['Versions'] = counts

kernels_notebooks.to_csv("Filter_Kernels_Url_Notebooks_Versions.csv",index=False)

#with open('kaggle_notebook_versions_count.csv','w') as file:
#    for notebook in notebooks:
#        file.write(f'{notebook[0]},{notebook[1]},{notebooks_dict.get(int(notebook[0]))}\n')