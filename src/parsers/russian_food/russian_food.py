import csv
import os
import random
import lxml
from time import sleep
from multiprocessing import Pool

import pandas as pd
import requests
from bs4 import BeautifulSoup

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


FILE_NAME = 'russianfood.csv'

most_common_user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
]

COLS = ['id', 'url', 'title', 'ingredients', 'steps', 'images']


def append_row(row):
    with open(FILE_NAME, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(row)
        
def get_https_proxies():

    proxies_resp = requests.get("https://free-proxy-list.net")
    soup_proxies = BeautifulSoup(proxies_resp.text, features="lxml")
    soup_proxies.find('table', {'id': 'proxylisttable'})
    rows = soup_proxies.find('table', {'id': 'proxylisttable'}).select('tr')
    proxies_data = []
    for row in rows[1: -1]:
        ip = row.find_all('td')[0].text
        port = row.find_all('td')[1].text
        code = row.find_all('td')[2].text
        country = row.find_all('td')[3].text
        anonimity = row.find_all('td')[4].text
        google = row.find_all('td')[5].text == 'yes'
        https = row.find_all('td')[6].text == 'yes'

        proxies_data.append({
            'ip': ip,
            'port': port,
            'code': code,
            'country': country,
            'anonimity': anonimity,
            'google': google,
            'https': https
        })


    
    # https_proxies = [f"{proxy['ip']}:{proxy['port']}" for proxy in proxies_data if proxy['https']]
    all_proxies = [f"{proxy['ip']}:{proxy['port']}" for proxy in proxies_data]
    
    return all_proxies

def get_url_with_proxy(url):
    global proxies
    counter = 0
    while True:
        useragent = random.choice(most_common_user_agents)
        proxy = random.choice(proxies)

        payload = {
            "proxies": {"http": proxy, "https": proxy},
            "url": url,
            "verify": False,
            "timeout": 2,
            "headers": {
                "User-Agent": useragent,
                "referrer": "https://yandex.ru",
            },
        }
        try:
            response = requests.get(**payload)
            if response.status_code == 200:
                break
        except:
            pass
        
        counter += 1
        if counter > 50:
            proxies = get_https_proxies()
            
    return response

def get_recipe(url):

    rid = int(url.split('recipe.php?rid=')[-1])

    response = get_url_with_proxy(url)
    soup = BeautifulSoup(response.text, features="lxml")

    title = soup.select_one('.recipe_new h1.title').text

    ingr_nodes = soup.select('#from .ingr .ingr_tr_0 td span')
    ingr = [i.text for i in ingr_nodes]

    step_text_nodes = soup.select('.step_images_n .step_n p')
    step_texts = [i.text.replace('\r\n', ' ').replace('\n', ' ').replace('  ', ' ') for i in step_text_nodes]


    step_img_nodes = soup.select('.step_images_n .step_n .img_c .tozoom')
    step_image_urls = ['https:' + i['href'] for i in step_img_nodes]
    img_names = []
    for i, image_url in enumerate(step_image_urls):
        file_ext = image_url.split('.')[-1]
        img_name = f"images/{rid}_{i}.{file_ext}"
        if not os.path.isfile(img_name):
            response_img = requests.get(image_url)
            if response_img.status_code == 200:
                img_names.append(img_name)
                with open(img_name, 'wb') as f:
                    f.write(response_img.content)
            else:
                img_names.append('')
        else:
            img_names.append(img_name)
            

    row = [
        rid,
        url,
        title,
        '||'.join(ingr),
        '||'.join(step_texts),
        '||'.join(img_names),
    ]
    return row


def run():
    global proxies
    if not os.path.isfile(FILE_NAME):
        append_row(COLS)
    
    if not os.path.isdir('images'):
        os.mkdir('images')

    for page in range(1, 592):
        proxies = get_https_proxies()

        page_url = f'https://www.russianfood.com/recipes/bytype/?fid=99&page={page}'
        response_page = requests.get(page_url)
        soup_page = BeautifulSoup(response_page.text, features="lxml")

        page_nodes = soup_page.select('.recipe_list_new .title_o .title a')
        page_links = ['https://www.russianfood.com' + n['href'] for n in page_nodes]

        print(f'Page: {page}')

        with Pool(16) as pool:
            rows = pool.map(get_recipe, page_links)

        for row in rows:
            append_row(row)
            
            
proxies = get_https_proxies()

if __name__ == '__main__':
    pass


