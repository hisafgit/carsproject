import requests
import time
import asyncio
from stack_logger import logger
from bs4 import BeautifulSoup
import sys
import re


class List:
    ''' Represents a page with list of items '''
    
    def __init__(self, base_url, path, **params):
        self.base_url = base_url
        self.path = path 
        self.items = []
        self.params = params

    def request_page(self):
        url = self.base_url + self.path
        logger.info(f"Requesting... {url}")
        res = requests.get(url, params=self.params)
        if res.status_code == 200:
            return res.text
        else:
            logger.error(f'No good response from {url}')

    def add_page(self):
        self.text = self.request_page()

    async def add_page_async(self):
        await asyncio.to_thread(self.add_page)
    
    def parse_page(self, parser="html.parser", html_tag="a", css_class="vehicle-card-link js-gallery-click-link"):
        soup = BeautifulSoup(self.text, parser)
        tag_list = soup.find_all(html_tag, class_=css_class)
        if len(tag_list):
            for tag in tag_list:
                item_detail_path = tag["href"]
                detail = Detail(base_url=self.base_url, path=item_detail_path)
                self.items.append(detail)
        else:
            logger.error('No item found!')

    

class Detail(List):

    def __init__(self, base_url, path, **params):
        super().__init__(base_url, path, **params)

    def parse_detail_old(self):
        if hasattr(self, "text"):
            soup = BeautifulSoup(self.text, 'html.parser')
            detail_section = soup.find("section", class_="sds-page-section basics-section")
            detail_elements = detail_section.find_all('dt')
            detail_dict = {}
            for key in detail_elements:
                detail_dict[key.get_text()] = key.next_sibling.next_sibling.get_text().strip()
            return detail_dict
        else:
            sys.exit('No text attached!')

    async def parse_detail_page_async(self):
        return await asyncio.to_thread(self.parse_detail_page)

    def parse_detail_page(self):
        ext_clr_rgx = re.compile(r'(?i)exterior color')
        trn_rgx = re.compile(r'(?i)transmission')
        year_and_brand_rgx = re.compile(r'(\d\d\d\d)\n    (.*)\n')
        soup = BeautifulSoup(self.text, 'html.parser')
        extcolor = soup.find("dt", string=ext_clr_rgx).next_sibling.next_sibling.get_text().strip()
        trans = soup.find("dt", string=trn_rgx).next_sibling.next_sibling.get_text().strip()
        img_url = soup.find('img', class_="swipe-main-image image-index-0")["src"]
        price = int(soup.find('span', class_='primary-price').text.replace(',','').strip('$'))
        title = soup.find('h1', class_='listing-title').text
        year_and_brand = year_and_brand_rgx.search(soup.find('div', class_="consumer-reviews-subheading").find('strong').text)
        year = int(year_and_brand.group(1))
        brand = year_and_brand.group(2)
        detail_dict = {'title':title, 'price':price, 'img_url':img_url, 
                       'brand':brand, 'year':year, 'extcolor':extcolor, 'trans':trans}
        return detail_dict 

    async def return_dict(self):
        await self.add_page_async()
        return await self.parse_detail_page_async()





base_url = 'https://www.cars.com'
listings_path = '/shopping/results/' 

async def main():
    # t_start = time.perf_counter()
    for page in range(20):
        l = List(base_url=base_url, path=listings_path, page=page, page_size=20)
        l.add_page()
        l.parse_page()
        L = await asyncio.gather(*[i.return_dict() for i in l.items])
        print(L)

    # t_end = time.perf_counter()
    # print(f"Total time taken: {t_end - t_start}s")

asyncio.run(main())

# RUNS OK