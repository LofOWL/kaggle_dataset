import pandas as pd
import numpy as np

Kernel_versions = pd.read_csv("Filter_Kernels_Url_Notebooks_Versions.csv")

print(Kernel_versions)

less_10 = Kernel_versions[Kernel_versions['TotalVotes'] >= 3]

more_versions = less_10[less_10['Versions'] >= 10]

more_versions.to_csv("Tmp.csv",index=False)
