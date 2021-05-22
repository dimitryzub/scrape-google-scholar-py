from serpapi import GoogleSearch
import os

def serpapi_srape_author_articles_results():
  params = {
    "api_key": os.getenv("API_KEY"),
    "engine": "google_scholar_author",
    "author_id": "9PepYk8AAAAJ",
    "hl": "en",
  }

  search = GoogleSearch(params)
  results = search.get_dict()

  for article in results['articles']:
    article_title = article['title']
    article_link = article['link']
    article_authors = article['authors']
    article_publication = article['publication']
    cited_by = article['cited_by']['value']
    cited_by_link = article['cited_by']['link']
    article_year = article['year']

    print(f"Title: {article_title}\nLink: {article_link}\nAuthors: {article_authors}\nPublication: {article_publication}\nCited by: {cited_by}\nCited by link: {cited_by_link}\nPublication year: {article_year}\n")
