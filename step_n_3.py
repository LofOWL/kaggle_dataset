from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import *
from selenium.webdriver.chrome.options import Options
import requests

from bs4 import BeautifulSoup 

from tqdm import tqdm
import time

class reader:

    def __init__(self,head=False,proxy=False):
        options = Options()
        if not head : options.add_argument('--headless')
        if proxy : options.proxy = proxy
        self.driver = webdriver.Chrome("./chromedriver",chrome_options=options)
        #self.driver = webdriver.Chrome("./chromedriver")

    def set_proxy(self,proxy):
        myProxy = "149.215.113.110:70"
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': myProxy,
            'sslProxy': myProxy,
            'noProxy': ''})
        return proxy

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
        divs = soup.find_all("div", {"class": "mdc-menu sc-kHWWYL eVshDL sc-jPfriQ eKezGi mdc-menu-surface"})
        urls = [a['href'] for div in divs for a in div.find_all('a',href=True)]
        versions_id = [url.split("scriptVersionId=")[-1] for url in urls if "scriptVersionId=" in url]

        if len(versions_id) >= 2:
            version_index = 1
            while versions_id:
                version = versions_id.pop()
                download_url = f'http://www.kaggle.com/kernels/scriptcontent/{version}/download'
                html = requests.get(download_url)
                with open(f"/media/lofowl/My Passport/2_kaggle_notebooks/{self.name}_{version_index}.txt","a+") as file:
                #with open(f"./notebooks/{self.name}_{version_index}.txt","a+") as file:
                    file.write(html.text)
                version_index += 1

    def close(self):
        self.driver.close()

    def urls(self):
        with open("url_kaggle_notebook.csv","r") as file:
            urls = file.read().split("\n")[:-1]
        return urls

def main(url):
    try:
        unit_run(url)
        print(f'done {url}')
        return [url,1]
    except:
        print(f'file {url}')
        return [url,-1]

def unit_run(input):
    url = input[0]
    proxy = input[1]
    r = reader(head=True,proxy=proxy)
    r.set_notebook_name(url)
    is_notebook = r.read()
    if is_notebook: 
        r.click()
        r.close()
    else:
        r.close()

if __name__ == "__main__":
    import multiprocessing
    r = reader()
    urls = r.urls()

    proxy_list = ['209.127.191.180:9279','45.95.96.187:8746','45.95.96.237:8796','193.8.127.189:9271','45.142.28.83:8094','45.136.231.43:7099','45.94.47.108:8152','193.8.56.119:9183','45.95.99.226:7786','45.95.99.20:7580']
    input = [(urls[i],proxy_list[i%10]) for i in range(len(urls))]

    with multiprocessing.Pool(processes=3) as pool:
        result = pool.map(main,input)

    with open('log_download.txt','a+') as file:
        for re in result:
            file.write(f'{re}\n')
    r.close()