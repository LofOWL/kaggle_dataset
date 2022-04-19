import pandas as pd
import numpy as np

Kernels_Url = pd.read_csv("Kernel_Url.csv")

if __name__ == "__main__":
    print(Kernels_Url)

    more_votes = Kernels_Url[Kernels_Url['TotalVotes'] >= 1]
    
    is_notebooks = more_votes[more_votes['Language'] == 8]

    print(is_notebooks)

    is_notebooks.to_csv("Filter_Kernels_Url_Notebooks.csv",index=False)
