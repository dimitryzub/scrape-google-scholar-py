from serpapi import GoogleSearch
import os

def serpapi_srape_cite_results():
  params = {
    "api_key": os.getenv("API_KEY"),
    "engine": "google_scholar_cite",
    "q": "FDc6HiktlqEJ"
  }

  search = GoogleSearch(params)
  results = search.get_dict()

  for cite in results['citations']:
    print(f'Title: {cite["title"]}\nSnippet: {cite["snippet"]}\n')
