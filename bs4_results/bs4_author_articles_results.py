from bs4 import BeautifulSoup
import requests, lxml

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

proxies = {
  'http': env.'HTTP_PROXY'
}

def bs4_srape_author_articles_result():
  html = requests.get('https://scholar.google.com/citations?hl=en&user=m8dFEawAAAAJ', headers=headers, proxies=proxies).text
  soup = BeautifulSoup(html, 'lxml')

  for article_info in soup.select('#gsc_a_b .gsc_a_t'):
    title = article_info.select_one('.gsc_a_at').text
    title_link = article_info.select_one('.gsc_a_at')['data-href']
    authors = article_info.select_one('.gsc_a_at+ .gs_gray').text
    publications = article_info.select_one('.gs_gray+ .gs_gray').text

    print('Article info:')
    print(f'Title: {title}\nTitle link: https://scholar.google.com{title_link}\Article Author(s): {authors}\Article Publication(s): {publications}\n')
