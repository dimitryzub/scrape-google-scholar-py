# This code block scrape Author info, Articles, Cited by block, Co-Authors

from serpapi import GoogleSearch
import os

def serpapi_srape_author_result():
  params = {
    "api_key": os.getenv("API_KEY"),
    "engine": "google_scholar_author",
    "author_id": "m8dFEawAAAAJ",
    "hl": "en",
  }

  search = GoogleSearch(params)
  results = search.get_dict()

  # Author info
  name = results['author']['name']
  affiliations = results['author']['affiliations']
  email = results['author']['email']
  interests1 = results['author']['interests'][0]['title']
  interests2 = results['author']['interests'][1]['title']

  print('Author Info:')
  print(f'{name}\n{affiliations}\n{email}\n{interests1}\n{interests2}\n')

  # Articles Results
  for article in results['articles']:
    article_title = article['title']
    article_link = article['link']
    article_authors = article['authors']
    article_publication = article['publication']
    cited_by = article['cited_by']['value']
    cited_by_link = article['cited_by']['link']
    article_year = article['year']

    print('Articles Info:')
    print(f"Title: {article_title}\nLink: {article_link}\nAuthors: {article_authors}\nPublication: {article_publication}\nCited by: {cited_by}\nCited by link: {cited_by_link}\nPublication year: {article_year}\n")

  # Cited By and Public Access Results
  citations_all = results['cited_by']['table'][0]['citations']['all']
  citations_2016 = results['cited_by']['table'][0]['citations']['since_2016']
  h_inedx_all = results['cited_by']['table'][1]['h_index']['all']
  h_index_2016 = results['cited_by']['table'][1]['h_index']['since_2016']
  i10_index_all = results['cited_by']['table'][2]['i10_index']['all']
  i10_index_2016 = results['cited_by']['table'][2]['i10_index']['since_2016']

  print('Citations Info:')
  print(f'{citations_all}\n{citations_2016}\n{h_inedx_all}\n{h_index_2016}\n{i10_index_all}\n{i10_index_2016}\n')

  public_access_link = results['public_access']['link']
  public_access_available_articles = results['public_access']['available']

  print('Public Access Info:')
  print(f'{public_access_link}\n{public_access_available_articles}\n')

  # Co-Authors Results
  for authors in results['co_authors']:
    author_name = authors['name']
    author_affiliations = authors['affiliations']
    author_link = authors['link']

    print('Co-Authour(s):')
    print(f'{author_name}\n{author_affiliations}\n{author_link}\n')
