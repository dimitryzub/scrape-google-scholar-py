from bs4 import BeautifulSoup
import requests, lxml

headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
}


def bs4_scrape_author_co_authors_result():
  html = requests.get('https://scholar.google.com/citations?hl=en&user=m8dFEawAAAAJ', headers=headers).text

  soup = BeautifulSoup(html, 'lxml')

  for container in soup.select('.gsc_rsb_aa'):
    author_name = container.select_one('#gsc_rsb_co a').text
    author_affiliations = container.select_one('.gsc_rsb_a_ext').text
    author_link = container.select_one('#gsc_rsb_co a')['href']
    print(f'{author_name}\n{author_affiliations}\nhttps://scholar.google.com{author_link}\n')
    
    
bs4_scrape_author_co_authors_result()
