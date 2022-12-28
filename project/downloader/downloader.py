import requests
import time
import asyncio
from bs4 import BeautifulSoup
import sys
import re
import os
import django
from django.db import utils
from custom_logger import logger
grandparent_dir = os.path.dirname(os.path.dirname(__file__))
target_dir = os.path.join(grandparent_dir, 'backend')
sys.path.append(target_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
from cars.models import Brand, ExteriorColor, Transmission, Car


class List:
    ''' Represents a page with list of items '''
    
    def __init__(self, base_url, path, **params):
        self.base_url = base_url
        self.path = path 
        self.url = base_url + path
        self.items = []
        self.params = params

    def request_page(self):
        logger.info(f"Requesting... {self.url} with {self.params}")
        res = requests.get(self.url, params=self.params)
        if res.status_code == 200:
            return res.text
        else:
            logger.error(f'No good response from {self.url}')

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
            logger.error(f'No items found on {self.url}')

    

class Detail(List):

    def __init__(self, base_url, path, **params):
        super().__init__(base_url, path, **params)

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
    
    async def parse_detail_page_async(self):
        return await asyncio.to_thread(self.parse_detail_page)
    
    async def add_dict(self):
        await self.add_page_async()
        return await self.parse_detail_page_async()

    async def save_to_db(self):
        await self.add_page_async()
        try:
            detail_dict = await self.parse_detail_page_async()
            task1 = await Brand.objects.aget_or_create(name = detail_dict.get('brand'))
            task2 = await ExteriorColor.objects.aget_or_create(color = detail_dict.get('extcolor'))
            task3 = await Transmission.objects.aget_or_create(transmission_type = detail_dict.get('trans'))
            try:
                task4 = await Car.objects.aget_or_create(title = detail_dict.get('title'), \
                    price = detail_dict.get('price'), img_url = detail_dict.get('img_url'), \
                        brand = task1[0], year = detail_dict.get('year'), \
                            extcolor = task2[0], trans = task3[0])
                if task4[1] == True:
                    logger.info(f'Details saved to db successfully for {self.url}')
                else:
                    logger.info(f'Details already exist on DB for {self.url}')
            except utils.IntegrityError:
                logger.info(f'Details already exist on DB for {self.url}')
        except ValueError:
            logger.warning(f'Detail dict could not be created for {self.url}')
    


base_url = 'https://www.cars.com'
listings_path = '/shopping/results/' 


async def main():
    
    for page in range(20):
        t_start = time.perf_counter()
        l = List(base_url=base_url, path=listings_path, page=page, page_size=20)
        l.add_page()
        l.parse_page()
        await asyncio.gather(*[i.save_to_db() for i in l.items])
        t_end = time.perf_counter()
        print(f"Total time taken: {t_end - t_start}s")

asyncio.run(main())

# RUNS OK