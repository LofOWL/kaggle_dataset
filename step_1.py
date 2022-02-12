import subprocess
import pandas as pd
from tqdm import tqdm

class reader:

    def __init__(self,page):
        self.page = page
        
    def read(self):
        command = f"kaggle kernels list --kernel-type 'notebook' --sort-by 'voteCount' --page-size 100 -p {self.page}"
        output = subprocess.getoutput(command)
        print(output)
        output = output.split("\n")[2:]
        result = list()
        for line in output:
            line = line.split("  ")
            line = [i for i in line if i != ""]
            line.append(str(self.page))
            result.append(line)
        return result

    def write(self):
        output = self.read()
        with open('kaggle_notebook_view_count.csv','a+') as file:
            for line in output:
                file.write(",".join(line)+'\n')

    def next(self):
        self.page += 1

if __name__ == "__main__":
    print("step 1")
    start_page = 12
    rd = reader(start_page)
    rd.write() 