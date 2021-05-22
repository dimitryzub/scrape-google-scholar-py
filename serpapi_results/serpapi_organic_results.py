from serpapi import GoogleSearch
import os, json

def serpapi_srape_organic_results():
  params = {
    "api_key": os.getenv("API_KEY"),
    "engine": "google_scholar",
    "q": "samsung",
  }

  search = GoogleSearch(params)
  results = search.get_dict()

  # It looks a bit akward but the point is that you can grab everything you need in 2-3 lines of code as below.
  for result in results['organic_results']:
    print(f"Title: {result['title']}\nPublication info: {result['publication_info']['summary']}\nSnippet: {result['snippet']}\nCited by: {result['inline_links']['cited_by']['link']}\nRelated Versions: {result['inline_links']['related_pages_link']}\n")

  # Or if you want more readable code, here's one example.
  data = []

  for result in results['organic_results']:
    data.append({
      'title': result['title'],
      'publication_info': result['publication_info']['summary'],
      'snippet': result['snippet'],
      'cited_by': result['inline_links']['cited_by']['link'],
      'related_versions': result['inline_links']['related_pages_link'],
    })

  print(json.dumps(data, indent = 2, ensure_ascii = False))
