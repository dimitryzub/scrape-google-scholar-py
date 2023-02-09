# custom backend
from custom_backend.google_scholar_profiles_results import scrape_google_scholar_profiles
from custom_backend.google_scholar_author_info_all_articles import scrape_google_scholar_author_data
from custom_backend.google_scholar_organic_search import scrape_google_scholar_organic_results
from custom_backend.google_scholar_top_mandates_metrics import google_scholar_top_mandates_metrics
from custom_backend.google_scholar_top_publications_metrics import google_scholar_top_publication_metrics

# serpapi backend
from serpapi_backend.serpapi_google_scholar_organic_results import serpapi_scrape_google_scholar_organic_results
from serpapi_backend.serpapi_google_scholar_organic_cite_results import serpapi_scrape_google_scholar_cite_results
from serpapi_backend.serpapi_google_scholar_profile_results import serpapi_scrape_google_scholar_profile_results
from serpapi_backend.serpapi_google_scholar_author_results import serpapi_scrape_google_scholar_author_results


'''
Custom backend

Google Scholar search operators could also be used:
    label:computer_vision "Michigan State University"|"U.Michigan"

This will search all profiles from 2 universities based on computer vision query
'''
# data = scrape_google_scholar_profiles(query='label:computer_vision "Michigan State University"|"U.Michigan"', pagination=False, operating_system='win')
# data = scrape_google_scholar_author_data(user_id='I1wOjTYUyYAC', operating_system='win') # or 'windows'
# data = google_scholar_top_mandates_metrics(operating_system='win', save_to_csv=True)
data = google_scholar_top_publication_metrics(operating_system='win', save_to_csv=True)
print(data)

# data = scrape_google_scholar_organic_results(query='blizzard effects xanax', pagination=False, operating_system='win', save_to_json=True)

# for profile in data:
#     print(profile['name'])
#     print(profile['interests'])

# print(json.dumps(data, indent=2))

'''
SerpApi backend

Same as in the custom backend, Google Scholar search operators could be used also.
'''

data = serpapi_scrape_google_scholar_cite_results(
        query='minecraft',
        api_key='...',
        pagination=False,
        lang='en'
    )
    
# extracting bottom links
for result in data:
    for citations in result['links']: 
        print(citations['name']) # or ['link']

# extracting citations
for result in data:
    for citations in result['citations']: 
        print(citations['title']) # or ['snippet']      