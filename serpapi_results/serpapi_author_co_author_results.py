from serpapi import GoogleScholarSearch
import os

def serpapi_srape_author_co_author_results():
  params = {
    "api_key": os.getenv("API_KEY"),
    "engine": "google_scholar_author",
    "author_id": "m8dFEawAAAAJ",
    "hl": "en",
  }

  search = GoogleScholarSearch(params)
  results = search.get_dict()

  for authors in results['co_authors']:
    author_name = authors['name']
    author_affiliations = authors['affiliations']
    author_link = authors['link']
    print(f'{author_name}\n{author_affiliations}\n{author_link}\n')
