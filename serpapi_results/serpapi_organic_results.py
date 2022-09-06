from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import os, json

def serpapi_scrape_google_scholar_organic_results():
    params = {
        # https://docs.python.org/3/library/os.html
        'api_key': os.getenv('API_KEY'), # serpapi api key
        'engine': 'google_scholar',      # serpapi parsing engine
        'q': 'blizzard',                 # search query
        'hl': 'en',                      # language
        'start': 0                       # first page
    }

    search = GoogleSearch(params)        # where data extracts on the backend

    organic_results_data = []

    while True:
        results = search.get_dict()       # JSON -> Python dict

        print(f'Currently extracting page #{results["serpapi_pagination"]["current"]}..')

        for result in results['organic_results']:
            position = result['position']
            title = result['title']
            publication_info_summary = result['publication_info']['summary']
            result_id = result['result_id']
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
              'page_number': results['serpapi_pagination']['current'],
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
            break

    return organic_results_data
