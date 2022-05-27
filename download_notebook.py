from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup 

from datetime import datetime

import requests

class Collector:

    def __init__(self,head=False):
        options = Options()
        if not head : options.add_argument('--headless')
        self.driver = webdriver.Chrome("./chromedriver",chrome_options=options)
    
    def set_download_path(self,path):
        self.download_path = path

    def set_notebook_name(self,name):
        self.name = name.replace("/","#")

    def set_time(self,time):
        self.filter_time = time

    def read(self):
        url = self.name.replace("#","/")
        kaggle_url = f"https://www.kaggle.com/{url}"
        self.driver.get(kaggle_url)
    
    def click(self):
        self.driver.find_element_by_xpath('//*[@id="site-content"]/div[3]/div[6]/div[1]/div/button').click()
        # collect the versions id
        soup = BeautifulSoup(self.driver.page_source,'html.parser')
        urls = [a['href'] for a in soup.find_all('a',href=True) if "scriptVersionId=" in a['href']]
        versions_id = [url.split("scriptVersionId=")[-1] for url in urls if "scriptVersionId=" in url]

        # collect the time 
        times = []
        for version in range(1,len(versions_id)+1):
            self.driver.find_element_by_xpath(f'//*[@id="site-content"]/div[3]/div[6]/div[10]/div[1]/div[2]/div[2]/div/div[2]/ul/div[{version}]').click()
            times.append(self.driver.find_element_by_xpath('//*[@id="site-content"]/div[3]/div[6]/div[10]/div[1]/div[1]/div[1]/span').text.split("•")[-1].strip())
        print(times)
        times = list(map(lambda x:datetime.strptime(x,'%b %d, %Y, %I:%M %p'),times))

        # merge id with time
        versions_times = list(zip(versions_id,times))
        filter_time = datetime.strptime(self.filter_time,'%b %d, %Y, %I:%M %p') if self.filter_time != None else datetime.now() 
        filter_versions_times = [id for id,time in versions_times if time <= filter_time]

        # download the notebook
        download_url = f'http://www.kaggle.com/kernels/scriptcontent/{filter_versions_times[0]}/download'
        html = requests.get(download_url)
        with open(f"{self.download_path}/{self.name}.ipynb","a+") as file: file.write(html.text)

    def close(self):
        self.driver.close()

    def download(self,url,time=None):
        self.set_notebook_name(url)
        self.set_time(time)
        self.read()
        self.click()

# renokan/pppm-deberta-v3-large-additional-fold-s

if __name__ == "__main__":
    c = Collector(True)
    c.set_download_path('/home/lofowl/Desktop/kaggle_dataset/notebooks')
    c.download("renokan/pppm-deberta-v3-large-additional-fold-s",'May 22, 2022, 8:28 PM')