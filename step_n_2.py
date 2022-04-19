from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import *
from selenium.webdriver.chrome.options import Options

import pandas as pd

from bs4 import BeautifulSoup 

from tqdm import tqdm

class reader:

    def __init__(self,head=False,proxy=False):
        self.options = Options()
        if not head : self.options.add_argument('--headless')
        if proxy : self.options.proxy = proxy
        self.driver = webdriver.Chrome("./chromedriver",chrome_options=self.options)
        #self.driver = webdriver.Chrome("./chromedriver")

    def set_proxy(self,proxy):
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxy,
            'sslProxy': proxy,
            'noProxy': ''})
        self.options.proxy = proxy

    def set_notebook_name(self,name):
        self.name = name.replace("/","#")

    def read(self):
        url = self.name.replace("#","/")
        kaggle_url = f"https://www.kaggle.com/{url}"
        self.driver.get(kaggle_url)


        is_notebook = self.driver.find_element_by_xpath('//*[@id="site-content"]/div[3]/div[4]/div/div[1]/div/button[1]/div/span[1]')
        is_notebook = is_notebook.text == "Notebook"
        return is_notebook

    def click(self):
        self.driver.find_element_by_xpath('//*[@id="site-content"]/div[3]/div[5]/div[1]/div/button').click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div[3]/div[5]/div[10]/div[1]/div[2]/div[2]/div/div[2]/ul/div[1]')))

        soup = BeautifulSoup(self.driver.page_source,'html.parser')
        divs = soup.find_all('a', href=True)
        urls = [a['href'] for a in divs]

        versions_id = [str(url.split("scriptVersionId=")[-1]) for url in urls if "scriptVersionId=" in url]
        if len(versions_id) >= 2:
            with open("notebooks_version_id.txt","a+") as file:
                file.write(f'{self.name} {" ".join(versions_id)}\n')

    def close(self):
        self.driver.close()

    def urls(self):
        data = pd.read_csv("Filter_Kernels_Url_Notebooks_Versions.csv")
        #18109 + 1279 + 15894 + 10410 + 10073 +  16178 + 9107 + 10710 + 7976 + 7621 + 8946 +8330 + 7965 + 8297 + 8364
        urls = list(data["Url"])[149259:]
        return urls

def unit_run(input):
    url = input[0]
    proxy = input[1]
    r = reader(head=False,proxy=proxy)
    r.set_notebook_name(url)
    is_notebook = r.read()
    if is_notebook: 
        r.click()
        r.close()
    else:
        r.close()

if __name__ == "__main__":
    r = reader(head=False)
    urls = r.urls()

    proxy_list = ['209.127.191.180:9279','45.95.96.187:8746','45.95.96.237:8796','193.8.127.189:9271','45.142.28.83:8094','45.136.231.43:7099','45.94.47.108:8152','193.8.56.119:9183','45.95.99.226:7786','45.95.99.20:7580']
    inputs = [(urls[i],proxy_list[i%10]) for i in range(len(urls))]

    for input in tqdm(inputs):
        try:
            unit_run(input)
        except:
            pass
    r.close()