from serpapi import GoogleSearch
import os

def serpapi_srape_profile_results():
    params = {
        "api_key": os.getenv("API_KEY"),
        "engine": "google_scholar_profiles",
        "hl": "en",
        "mauthors": "samsung"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    for result in results['profiles']:
      name = result['name']
      try:
        email = result['email']
      except:
        email = None
      affiliation = result['affiliations']
      cited_by = result['cited_by']
      interests = result['interests'][0]['title']
      interests_link = result['interests'][0]['link']

      print(f'{name}\n{email}\n{affiliation}\n{cited_by}\n{interests}\n{interests_link}\n')
