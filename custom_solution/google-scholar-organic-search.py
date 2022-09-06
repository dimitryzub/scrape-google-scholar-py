from bs4 import BeautifulSoup
from parsel import Selector
import requests, lxml, os, json


def scrape_one_google_scholar_page():
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    params = {
        'q': 'samsung medical center seoul semiconductor element simulation x-ray fetch',
        'hl': 'en'
    }

    html = requests.get('https://scholar.google.com/scholar', headers=headers, params=params).text
    soup = BeautifulSoup(html, 'lxml')

    # JSON data will be collected here
    data = []

    # Container where all needed data is located
    for result in soup.select('.gs_r.gs_or.gs_scl'):
        title = result.select_one('.gs_rt').text
        title_link = result.select_one('.gs_rt a')['href']
        publication_info = result.select_one('.gs_a').text
        snippet = result.select_one('.gs_rs').text
        cited_by = result.select_one('#gs_res_ccl_mid .gs_nph+ a')['href']
        related_articles = result.select_one('a:nth-child(4)')['href']
        try:
            all_article_versions = result.select_one('a~ a+ .gs_nph')['href']
        except:
            all_article_versions = None
        
        try:
            pdf_link = result.select_one('.gs_or_ggsm a:nth-child(1)')['href']
        except: 
            pdf_link = None

        data.append({
            'title': title,
            'title_link': title_link,
            'publication_info': publication_info,
            'snippet': snippet,
            'cited_by': f'https://scholar.google.com{cited_by}',
            'related_articles': f'https://scholar.google.com{related_articles}',
            'all_article_versions': f'https://scholar.google.com{all_article_versions}',
            "pdf_link": pdf_link
        })

    print(json.dumps(data, indent = 2, ensure_ascii = False))



def google_scholar_pagination():
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    params = {
        'q': 'samsung medical center seoul semiconductor element simulation x-ray fetch',
        'hl': 'en',
        'start': 0
    }

    # JSON data will be collected here
    data = []

    while True:
        html = requests.get('https://scholar.google.com/scholar', headers=headers, params=params).text
        selector = Selector(text=html)

        print(f'extrecting {params["start"] + 10} page...')

        # Container where all needed data is located
        for result in selector.css('.gs_r.gs_or.gs_scl'):
            title = result.css('.gs_rt').xpath('normalize-space()').get()
            title_link = result.css('.gs_rt a::attr(href)').get()
            publication_info = result.css('.gs_a').xpath('normalize-space()').get()
            snippet = result.css('.gs_rs').xpath('normalize-space()').get()
            cited_by_link = result.css('.gs_or_btn.gs_nph+ a::attr(href)').get()

            data.append({
                'page_num': params['start'] + 10, # 0 -> 1 page. 70 in the output = 7th page
                'title': title,
                'title_link': title_link,
                'publication_info': publication_info,
                'snippet': snippet,
                'cited_by_link': f'https://scholar.google.com{cited_by_link}',
            })
        
        # bs4 had difficulties with this selector at the time I wrote this code, not 100% sure why
        if selector.css('.gs_ico_nav_next').get():
            params['start'] += 10
        else:
            break

    print(json.dumps(data, indent = 2, ensure_ascii = False))
