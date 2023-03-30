#TODO: support/refactor CITE extraction. This is not yet implemented.

from parsel import Selector
import requests

params = {
    'q': 'blizzard', # search query
    'hl': 'en'       # language of the search   
}


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'accept-language': 'en-US,en',
    'referer': f"https://scholar.google.com/scholar?hl={params['hl']}&q={params['q']}"
}


def parsel_get_cite_ids():
    html = requests.get('https://scholar.google.com/scholar', params=params, headers=headers)
    soup = Selector(text=html.text)

    # returns a list of publication ID's -> U8bh6Ca9uwQJ
    return soup.css('.gs_r.gs_or.gs_scl::attr(data-cid)').getall()

def parsel_scrape_cite_results():
    citations = []

    for cite_id in parsel_get_cite_ids():
        html = requests.get(f'https://scholar.google.com/scholar?output=cite&q=info:{cite_id}:scholar.google.com', headers=headers)
        selector = Selector(text=html.text)
         
        # might be issues in the future with extracting data from the table
        if selector.css('#gs_citt').get():
            for result in selector.css('tr'):
                institution = result.xpath('th/text()').get()
                citation = result.xpath('td div/text()').get()

                citations.append({'institution': institution, 'citations': citation})

    return citations
