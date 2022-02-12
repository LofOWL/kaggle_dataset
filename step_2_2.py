from curses.ascii import isdigit
from bs4 import BeautifulSoup
from selenium import webdriver

class reader:

    def __init__(self,index):
        self.index = index
        self.driver = webdriver.Chrome("./chromedriver")
        with open("error_kaggle_notebook.csv","r") as file:
            self.urls = file.read().split("\n")[:-1]
            self.urls = [i.split(",") for i in self.urls]
            self.urls = [i[0].strip() for i in self.urls]

    def read(self):
        kaggle_url = f"https://www.kaggle.com/{self.urls[self.index]}"
        print(kaggle_url)
        self.driver.get(kaggle_url)

    def extract_parameters(self):

        html = self.driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        # collect copy_edit & versions
        elements = soup.find_all("span", {"class": "sc-gXfVKN sc-cBoqAE jmJemH lRfdj"})
        elements = [i.text for i in elements]
        print(elements)
        copy_edit = elements[3]
        versions = [i for i in elements[4].split(" ") if i.isdigit()][0] if len(elements) >= 5 else 0

        # collect tags
        elements = soup.find_all("span", {"class": "sc-kLojOw sc-iklJeh eGLYxv hbusih"})
        tags = '%'.join([i.text for i in elements])

        # collect comment
        elements = soup.find_all("span", {"class": "sc-ezzafa sc-bYwzuL dfGXIV fDDjHD"})
        elements = [i.text for i in elements]
        comments = ''.join([i for i in elements[2] if i.isdigit()])

        return [copy_edit,versions,tags,comments]

    def write(self):
        try:
            self.read()
            result = self.extract_parameters()
            result.insert(0,self.urls[self.index])
            with open('error_kaggle_notebook_recollect.csv','a+') as file:
                file.write(','.join(result)+"\n")
        except:
            pass

    def next(self):
        self.index += 1
        return len(self.urls) - 1 >= self.index

def run(index_start):
    r = reader(index_start)
    r.write()
    isNext = r.next()
    while isNext:
        r.write()
        print(f'{r.index} done')
        isNext = r.next()
        print(f'{r.index} start')

if __name__ == "__main__":
    print("step_2_2.py")
    run(0)