from bs4 import BeautifulSoup
import requests, lxml

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

# extracts 10 profiles from the first page
def bs4_srape_profile_results():
  html = requests.get('https://scholar.google.com/citations?view_op=view_org&hl=en&org=9834965952280547731', headers=headers).text

  soup = BeautifulSoup(html, 'lxml')

  for result in soup.select('.gs_ai_chpr'):
    name = result.select_one('.gs_ai_name a').text
    link = result.select_one('.gs_ai_name a')['href']
    affiliations = result.select_one('.gs_ai_aff').text
    email = result.select_one('.gs_ai_eml').text
    try:
      interests = result.select_one('.gs_ai_one_int').text
    except:
      interests = None
    cited_by = result.select_one('.gs_ai_cby').text.split(' ')[2]
    
    print(f'{name}\nhttps://scholar.google.com{link}\n{affiliations}\n{email}\n{interests}\n{cited_by}\n')
