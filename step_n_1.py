import pandas as pd
from tqdm import tqdm
import multiprocessing

kernels = pd.read_csv("./meta_data/Kernels.csv")
kernel_versions = pd.read_csv("./meta_data/KernelVersions.csv")
users = pd.read_csv("./meta_data/Users.csv")
kernel_languages = pd.read_csv('./meta_data/KernelLanguages.csv')

def get_url(id):
    uid = int(kernels[kernels['Id'] == id]['AuthorUserId'].iloc[0])
    url = str(kernels[kernels['Id'] == id]['CurrentUrlSlug'].iloc[0])
    user_name = str(users[users['Id'] == uid]['UserName'].iloc[0])
    return f'{user_name}/{url}'

def is_notebooks(id):
    language_id = kernel_versions[kernel_versions['ScriptId'] == id]['ScriptLanguageId']
    language_id = list(set(language_id))[0]
    return language_id

def main(id):
    try:
        url = get_url(id)
        language_id = is_notebooks(id)
        print(f'done {url}')
        return [id,url,language_id]
    except:
        print(f'file {id}')
        return [id,-1,-1]

if __name__ == "__main__":
    all_ids = list(kernels['Id'])
    print(main(all_ids[0]))
    
    with multiprocessing.Pool(processes=10) as pool:
        all_urls = pool.map(main,all_ids)
    
    with open('url_kaggle_notebook.csv','a+') as file:
        for item in all_urls:
            file.write(f'{item[0]} {item[1]} {item[2]}\n')