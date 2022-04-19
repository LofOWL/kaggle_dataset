import pandas as pd
import numpy as np

if __name__ == "__main__":
    Kernels = pd.read_csv('./meta_data/Kernels.csv')

    Url = pd.read_csv('url_kaggle_notebook.csv',delimiter=r' ',names=['Id',"Url","Language"])
    Url = Url[['Url','Language']]

    merge = pd.concat([Kernels,Url],axis=1,join='inner')

    print(merge)

    merge.to_csv("Kernel_Url.csv",index=False)
