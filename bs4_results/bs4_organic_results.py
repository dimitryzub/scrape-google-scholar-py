from bs4 import BeautifulSoup
import requests, lxml, os, json

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

proxies = {
  'http': os.getenv('HTTP_PROXY')
}

def bs4_srape_organic_results():
  html = requests.get('https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=samsung&oq=', headers=headers, proxies=proxies).text

  soup = BeautifulSoup(html, 'lxml')

  # Scrape just PDF links
  # for pdf_link in soup.select('.gs_or_ggsm a'):
  #   pdf_file_link = pdf_link['href']
  #   print(pdf_file_link)
  
  # JSON Output
  data = []

  # Container where all needed data located
  for result in soup.select('.gs_ri'):
    title = result.select_one('.gs_rt').text
    publication_info = result.select_one('.gs_a').text
    snippet = result.select_one('.gs_rs').text
    cited_by = result.select_one('#gs_res_ccl_mid .gs_nph+ a')['href']
    related_articles = result.select_one('a:nth-child(4)')['href']
    all_article_versions = result.select_one('a~ a+ .gs_nph')['href']
    link = result.select_one('.gs_rt a')['href']

    data.append({
      'title': title,
      'publication_info': publication_info,
      'snippet': snippet,
      'cited_by': f'https://scholar.google.com{cited_by}',
      'related_articles': f'https://scholar.google.com{related_articles}',
      'all_article_versions': f'https://scholar.google.com{all_article_versions}',
      'link': link,
    })

  print(json.dumps(data, indent = 2, ensure_ascii = False))
