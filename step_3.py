from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup 

from tqdm import tqdm

class reader:

    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver")

    def set_notebook_name(self,name):
        self.name = name.replace("/","#")

    def read(self):
        url = self.name.replace("#","/")
        kaggle_url = f"https://www.kaggle.com/{url}"
        print(kaggle_url)
        self.driver.get(kaggle_url)

    def click(self):
        self.driver.find_element_by_xpath('//*[@id="site-content"]/div[3]/div[5]/div[1]/div/button').click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div[3]/div[5]/div[10]/div[1]/div[2]/div[2]/div/div[2]/ul/div[1]')))

        version_number = self.driver.find_element_by_xpath('//*[@id="site-content"]/div[3]/div[5]/div[10]/div[1]/div[1]/div[1]/span/span')
        version_number = int(version_number.text.split(" ")[-1])
        total = version_number + 1

        while version_number != 0:
            element = self.driver.find_element_by_xpath(f'//*[@id="site-content"]/div[3]/div[5]/div[10]/div[1]/div[2]/div[2]/div/div[2]/ul/div[{total-version_number}]')
            self.driver.execute_script("arguments[0].click();",element)


            #WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rendered-kernel-content"]')))
            #time.sleep(0.5)

            page = self.driver.page_source
            soup = BeautifulSoup(page,'html.parser')
            find_iframe = soup.find_all('iframe')
            print('done iframe detection')

            #notebook_iframe = self.driver.find_element_by_xpath('//*[@id="rendered-kernel-content"]')
            if len(find_iframe) == 2:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[1]/div/div[4]/div[3]/div[5]/div[10]/div[1]/div[2]/div[1]/div/div/div/div/iframe')))
                notebook_iframe = self.driver.find_element_by_xpath('/html/body/main/div[1]/div/div[4]/div[3]/div[5]/div[10]/div[1]/div[2]/div[1]/div/div/div/div/iframe')
                self.driver.switch_to.frame(notebook_iframe)
                notebook = self.driver.find_element_by_xpath('/html/body')
            else:
                notebook = self.driver.find_element_by_xpath('/html/body/main/div[1]/div/div[4]/div[3]/div[5]/div[10]/div[1]/div[2]/div[1]/div/div/div/pre/code')

            with open(f'/media/lofowl/My Passport/kaggle_notebooks/{self.name}_{version_number}.txt','a+') as file:
            #with open(f'./notebooks/{self.name}_{version_number}.txt','a+') as file:
                file.write(notebook.text)
            print(f'done {version_number}')

            self.driver.switch_to.default_content()
            version_number -= 1
            
    # //*[@id="rendered-kernel-content"]  

    def urls(self):
        with open("final_kaggle_notebook.csv","r") as file:
            file = file.read().split("\n")[:-1]
            lines = [i.split(",") for i in file]
            urls = [i[0] for i in lines]
            versions = [int(i[2]) for i in lines]
        return urls,versions

def run():
    r = reader()
    urls,versions = r.urls()
    urls = urls[19:]
    for url in tqdm(urls):
        try:
            r.set_notebook_name(url)
            r.read() 
            r.click()
        except:
            print(url)

def test():
    r = reader()
    urls,_ = r.urls()
    r.set_notebook_name(urls[19])
    r.read()
    r.click()

if __name__ == "__main__":
    print("step_3")
    run()
    #test()