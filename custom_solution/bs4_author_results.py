from bs4 import BeautifulSoup
import requests, lxml

headers = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
}

def bs4_scrape_author_result():
  html = requests.get('https://scholar.google.com/citations?hl=en&user=m8dFEawAAAAJ', headers=headers).text
  soup = BeautifulSoup(html, 'lxml')

  # Author info
  name = soup.select_one('#gsc_prf_in').text
  affiliation = soup.select_one('#gsc_prf_in+ .gsc_prf_il').text

  try:
    email = soup.select_one('#gsc_prf_ivh').text
  except:
    email = None

  try:
    interests = soup.select_one('#gsc_prf_int').text
  except:
    interests = None

  print('Author info:')
  print(f'{name}\n{affiliation}\n{email}\n{interests}\n')

  # Article info
  for article_info in soup.select('#gsc_a_b .gsc_a_t'):
    title = article_info.select_one('.gsc_a_at').text
    title_link = article_info.select_one('.gsc_a_at')['data-href']
    authors = article_info.select_one('.gsc_a_at+ .gs_gray').text
    publications = article_info.select_one('.gs_gray+ .gs_gray').text

    print('Article info:')
    print(f'Title: {title}\nTitle link: https://scholar.google.com{title_link}\Article Author(s): {authors}\Article Publication(s): {publications}\n')

  # Cited by and Public Access Info:
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
    
    # Co-Authors
    try:
      for container in soup.select('.gsc_rsb_aa'):
        author_name = container.select_one('#gsc_rsb_co a').text
        author_affiliations = container.select_one('.gsc_rsb_a_ext').text
        author_link = container.select_one('#gsc_rsb_co a')['href']

        print('Co-Author(s):')
        print(f'{author_name}\n{author_affiliations}\nhttps://scholar.google.com{author_link}\n')
    except:
      print('no co-authors found.')
