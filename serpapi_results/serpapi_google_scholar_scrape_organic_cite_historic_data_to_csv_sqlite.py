# https://serpapi.com/blog/scrape-historic-google-scholar-results-using-python/


import os
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl


def organic_results():
    print('Extracting organic results..')

    params = {
        'api_key': os.getenv('API_KEY'),
        'engine': 'google_scholar',
        'q': 'minecraft redstone system structure characteristics strength',  # search query
        'hl': 'en',        # language
        'as_ylo': '2017',  # from 2017
        'as_yhi': '2021',  # to 2021
        'start': '0'       # first page
    }

    search = GoogleSearch(params)

    organic_results_data = []

    loop_is_true = True

    while loop_is_true:
        results = search.get_dict()

        print(f"Currently extracting page №{results['serpapi_pagination']['current']}..")

        for result in results.get('organic_results', []):
            position = result.get('position')
            title = result.get('title')
            publication_info_summary = result.get('publication_info', {}).get('summary')
            result_id = result.get('result_id')
            link = result.get('link')
            result_type = result.get('type')
            snippet = result.get('snippet')
  
            try:
              file_title = result['resources'][0]['title']
            except: file_title = None
  
            try:
              file_link = result['resources'][0]['link']
            except: file_link = None
  
            try:
              file_format = result['resources'][0]['file_format']
            except: file_format = None
  
            try:
              cited_by_count = int(result['inline_links']['cited_by']['total'])
            except: cited_by_count = None
  
            cited_by_id = result.get('inline_links', {}).get('cited_by', {}).get('cites_id', {})
            cited_by_link = result.get('inline_links', {}).get('cited_by', {}).get('link', {})
  
            try:
              total_versions = int(result['inline_links']['versions']['total'])
            except: total_versions = None
  
            all_versions_link = result.get('inline_links', {}).get('versions', {}).get('link', {})
            all_versions_id = result.get('inline_links', {}).get('versions', {}).get('cluster_id', {})
  
            organic_results_data.append({
              'page_number': results.get('serpapi_pagination', {}).get('current'),
              'position': position + 1,
              'result_type': result_type,
              'title': title,
              'link': link,
              'result_id': result_id,
              'publication_info_summary': publication_info_summary,
              'snippet': snippet,
              'cited_by_count': cited_by_count,
              'cited_by_link': cited_by_link,
              'cited_by_id': cited_by_id,
              'total_versions': total_versions,
              'all_versions_link': all_versions_link,
              'all_versions_id': all_versions_id,
              'file_format': file_format,
              'file_title': file_title,
              'file_link': file_link,
            })

            if 'next' in results.get('serpapi_pagination', {}):
                search.params_dict.update(dict(parse_qsl(urlsplit(results['serpapi_pagination']['next']).query)))
            else:
                loop_is_true = False

    return organic_results_data
  
  

  
# Extracting cite data: https://serpapi.com/blog/scrape-historic-google-scholar-results-using-python/#cite_results
# if you already have a list of result id's

# result_ids = ["FDc6HiktlqEJ", "FDc6Hikt21J", "aSAF1ASHRJI"]
# for citation in result_ids:
#     params = {
#         "api_key": "API_KEY",             # SerpApi API key
#         "engine": "google_scholar_cite",  # cite results extraction
#         "q": citation                     # FDc6HiktlqEJ ... FDc6Hikt21J
#     }
#     
#     search = GoogleSearch(params)
#     results = search.get_dict()
      # further extraction code..

#TODO: add citation extraction
if __name__ == '__main__': 
    serpapi_scrape_google_scholar_organic_results()