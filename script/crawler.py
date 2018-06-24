import re
import yaml
from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from bs4 import BeautifulSoup
import time
from urllib.parse import urldefrag, urljoin

class Crawler:

    def __init__(self,driver_path,conf):
        self.conf = conf
        print(self.conf)

        self.crawled_urls = {}
        self.crawl_que = [[]]
        self.item_que = []

        # options = webdriver.ChromeOptions()
        # options.set_headless()
        # self.driver = webdriver.Chrome(
        #     driver_path
        #     ,chrome_options = options
        # )

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--screen-size=1200x800")

        self.driver = webdriver.Remote(
            command_executor = driver_path,
            desired_capabilities=options.to_capabilities()
        )

    def select_link(self,links,allow,deny):
        matched = []
        for link in links:
            flag = False
            for ptn in allow:
                if re.match(ptn,link):
                    flag = True
                    break 
            for ptn in deny:
                if re.match(ptn,link):
                    flag = False
                    break        
            if flag:
                matched.append(link)
        return matched

    def run_crawler(self, urls, depth):
        # confのdepthに到達したらクローリングを終了する
        if(self.conf['crawling_setting']['depth'] + 1 == depth):
            return
        
        for url in urls:
            if url in self.crawled_urls:
                continue
            
            print("crawling depth:",depth,"url:", url)
            self.driver.get(url)
            time.sleep(1)

            self.crawled_urls[url]=True

            links = []
            for elem_a in self.driver.find_elements_by_tag_name('a'):
                links.append(urljoin(url,elem_a.get_attribute("href")))

            self.crawl_que[depth].extend(
                self.select_link(
                    links
                    ,self.conf['crawling_setting']['crawl_url']['allow']
                    ,self.conf['crawling_setting']['crawl_url']['deny']
                )
            )

            self.item_que.extend(
                self.select_link(
                    links
                    ,self.conf['crawling_setting']['scrap_url']['allow']
                    ,self.conf['crawling_setting']['scrap_url']['deny']
                )
            )
                
        self.crawl_que.append([])
        self.run_crawler(self.crawl_que[depth],depth+1)
        return

    def run(self):
        self.run_crawler(self.conf['crawling_setting']['top_url'],0)
        print("item_que:", self.item_que)
        self.run_scraper()
        return

    def get_desc(self, desc_name):
        desc_set = []
        for elem_desc_xpath in self.driver.find_elements_by_xpath(self.conf['scraping_setting'][desc_name]['xpath']):
            desc_set.append(elem_desc_xpath.text)
        return(' '.join(desc_set))
    
    def get_image_maxsize(self):
        img_size = {}
        for elem_img in self.driver.find_elements_by_tag_name('img'): 
            size = elem_img.size['height'] * elem_img.size['width']
            img_size[elem_img.get_attribute('src')] = size
        return(max(img_size.items(), key=lambda x:x[1])[0])

    def run_scraper(self):
        num = 0
        # 重複を削除したリストをループ
        for item_url in list(set(self.item_que)):
            num += 1
            if num > self.conf['scraping_setting']['limit']:
                break
            
            self.driver.get(item_url)   
            time.sleep(1)

            item_title = self.driver.title
            # 2(0+2)でホスト
            item_id = item_url.split("/")[self.conf['scraping_setting']['item_id']['url_path_seq']+2]
            item_img_size = self.get_image_maxsize()
            item_img_xpath = self.driver.find_element_by_xpath(self.conf['scraping_setting']['item_image']['xpath']).get_attribute('src')
            item_desc = self.get_desc('item_desc')
            item_desc2 = self.get_desc('item_desc2')
            item_desc3 = self.get_desc('item_desc3')

            print("------------------------------------")
            print("url:",item_url)
            print("id:",item_id)
            print("title:",item_title)
            print("img_size:",item_img_size)
            print("img_xpath:",item_img_xpath)
            print("desc:",item_desc)
            print("desc2:",item_desc2)
            print("desc3:",item_desc3)
            
        return
    
    def __def__(self):
        self.driver.close()
        print("driver close")
        self.driver.quit()
        print("driver quit")

conf = yaml.load(open("config.yml","r+"))
crw = Crawler(
    # "http://127.0.0.1:4444/wd/hub"
    "http://selenium-hub:4444/wd/hub"
    ,conf)
crw.run()
del crw

