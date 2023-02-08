from serpapi_backend.serpapi_google_scholar_organic_results import serpapi_scrape_google_scholar_organic_results
from serpapi import GoogleScholarSearch

def serpapi_scrape_google_scholar_cite_results(
        query: str,
        api_key: str = None,
        lang: str = 'en',
        pagination: bool = False 
    ):
    
    '''
    This function extract citations as well as BibTeX, EndNote, RefMan, RefWorks links.
    
    To extract citations, 2 requests has to be made: 1 for organic results, 2 for citation data. 
    So if you need to get citations from 1000 articles, 2000 requests would be made accordingly.
    
    Arguments:
    - query: search query
    - api_key: SerpApi api key, https://serpapi.com/manage-api-key
    - lang: language for the search, https://serpapi.com/google-languages
    - pagination: True of False. Enables pagination from all pages.
    
    Usage:
    
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
    '''
    
    if api_key is None:
        raise Exception('Please enter a SerpApi API key to a `api_key` argument. https://serpapi.com/manage-api-key')
    
    #TODO: could be removed as function by itself throw an error if query is missing
    if api_key and query is None:
        raise Exception('Please enter a SerpApi API key to a `api_key`, and a search query to `query` arguments.')
    
    organic_results = serpapi_scrape_google_scholar_organic_results(
        query=query,
        api_key=api_key,
        lang=lang,
        pagination=pagination
    )
    
    cite_results_data = []

    for citation in organic_results:
        params = {
            'api_key': api_key,              # serpapi api key: https://serpapi.com/manage-api-key
            'engine': 'google_scholar_cite', # serpapi parsing engine
            'q': citation['result_id']       # search query
        }
        
        search = GoogleScholarSearch(params) # where data extracts on the backend
        results = search.get_dict()
        
        # removes 2 keys from the JSON response 
        for key_to_delete in ['search_metadata', 'search_parameters']:
            results.pop(key_to_delete)
            
        if 'error' in results:
            raise Exception(results['error'])
            
        cite_results_data.append(results)

    return cite_results_data
