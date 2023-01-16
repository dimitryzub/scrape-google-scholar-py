# blog post: https://serpapi.com/blog/scrape-google-scholar-case-law-results-to-csv-with-python-and-serpapi/#code-explanation

import os
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import pandas as pd

def case_law_results():
    print('Extracting case law results..')

    params = {
        'api_key': os.getenv('API_KEY'),  # SerpApi API key
        'engine': 'google_scholar',       # Google Scholar search results
        'q': 'minecraft education ',      # search query
        'hl': 'en',                       # language
        'start': '0',                     # first page
        'as_sdt': '6'                     # case law results. Wierd, huh? Try without it.
    }
    search = GoogleSearch(params)

    case_law_results_data = []

    loop_is_true = True
    while loop_is_true:
      results = search.get_dict()

      print(f"Currently extracting page №{results['serpapi_pagination']['current']}..")

      for result in results['organic_results']:
        title = result['title']
        publication_info_summary = result['publication_info']['summary']
        result_id = result['result_id']
        link = result['link']
        result_type = result.get('type')
        snippet = result['snippet']

        try:
          file_title = result['resources'][0]['title']
        except: file_title = None

        try:
          file_link = result['resources'][0]['link']
        except: file_link = None

        try:
          file_format = result['resources'][0]['file_format']
        except: file_format = None

        cited_by_count = result.get('inline_links', {}).get('cited_by', {}).get('total', {})
        cited_by_id = result.get('inline_links', {}).get('cited_by', {}).get('cites_id', {})
        cited_by_link = result.get('inline_links', {}).get('cited_by', {}).get('link', {})
        total_versions = result.get('inline_links', {}).get('versions', {}).get('total', {})
        all_versions_link = result.get('inline_links', {}).get('versions', {}).get('link', {})
        all_versions_id = result.get('inline_links', {}).get('versions', {}).get('cluster_id', {})

        case_law_results_data.append({
          'page_number': results['serpapi_pagination']['current'],
          'position': result['position'] + 1,
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

        if 'next' in results['serpapi_pagination']:
          search.params_dict.update(dict(parse_qsl(urlsplit(results['serpapi_pagination']['next']).query)))
        else:
          loop_is_true = False

    return case_law_results_data


def save_case_law_results_to_csv():
    print('Waiting for case law results to save..')
    pd.DataFrame(data=case_law_results()).to_csv('google_scholar_case_law_results.csv', encoding='utf-8', index=False)

    print('Case Law Results Saved.')
