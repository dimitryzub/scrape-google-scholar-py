from bs4 import BeautifulSoup
import requests, lxml

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

def bs4_srape_author_citedby_result():
  html = requests.get('https://scholar.google.com/citations?hl=en&user=m8dFEawAAAAJ', headers=headers).text
  soup = BeautifulSoup(html, 'lxml')

  for cited_by_public_access in soup.select('.gsc_rsb'):
    citations_all = cited_by_public_access.select_one('tr:nth-child(1) .gsc_rsb_sc1+ .gsc_rsb_std').text
    citations_since2016 = cited_by_public_access.select_one('tr:nth-child(1) .gsc_rsb_std+ .gsc_rsb_std').text
    h_index_all = cited_by_public_access.select_one('tr:nth-child(2) .gsc_rsb_sc1+ .gsc_rsb_std').text
    h_index_2016 = cited_by_public_access.select_one('tr:nth-child(2) .gsc_rsb_std+ .gsc_rsb_std').text
    i10_index_all = cited_by_public_access.select_one('tr~ tr+ tr .gsc_rsb_sc1+ .gsc_rsb_std').text
    i10_index_2016 = cited_by_public_access.select_one('tr~ tr+ tr .gsc_rsb_std+ .gsc_rsb_std').text
    articles_num = cited_by_public_access.select_one('.gsc_rsb_m_a:nth-child(1) span').text.split(' ')[0]
    articles_link = cited_by_public_access.select_one('#gsc_lwp_mndt_lnk')['href']
    
    print('Citiation info:')
    print(f'{citations_all}\n{citations_since2016}\n{h_index_all}\n{h_index_2016}\n{i10_index_all}\n{i10_index_2016}\n{articles_num}\nhttps://scholar.google.com{articles_link}\n')
