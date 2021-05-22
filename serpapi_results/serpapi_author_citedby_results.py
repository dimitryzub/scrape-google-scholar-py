from serpapi import GoogleSearch
import os

def serpapi_srape_author_citedby_results():
  params = {
    "api_key": os.getenv("API_KEY"),
    "engine": "google_scholar_author",
    "author_id": "9PepYk8AAAAJ",
    "hl": "en",
  }

  search = GoogleSearch(params)
  results = search.get_dict()

  citations_all = results['cited_by']['table'][0]['citations']['all']
  citations_2016 = results['cited_by']['table'][0]['citations']['since_2016']
  h_inedx_all = results['cited_by']['table'][1]['h_index']['all']
  h_index_2016 = results['cited_by']['table'][1]['h_index']['since_2016']
  i10_index_all = results['cited_by']['table'][2]['i10_index']['all']
  i10_index_2016 = results['cited_by']['table'][2]['i10_index']['since_2016']

  print(f'{citations_all}\n{citations_2016}\n{h_inedx_all}\n{h_index_2016}\n{i10_index_all}\n{i10_index_2016}\n')

  public_access_link = results['public_access']['link']
  public_access_available_articles = results['public_access']['available']

  print(f'{public_access_link}\n{public_access_available_articles}\n')
