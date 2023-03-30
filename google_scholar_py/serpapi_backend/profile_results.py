from serpapi import GoogleScholarSearch
from urllib.parse import parse_qsl, urlsplit
import itertools


#TODO: support pagination using `async` parameter

class SerpApiGoogleScholarProfiles:
    def __init__(self) -> None:
        pass

    def scrape_google_scholar_profile_results(
            self,
            query: str,
            api_key: str = None,
            lang: str = 'en',
            pagination: bool = False,
        ):
        
        '''
        This function extracts profile results. With or without pagination.
        
        Arguments:
        - query: search query
        - api_key: SerpApi api key, https://serpapi.com/manage-api-key
        - lang: language for the search. Default 'en'. More: https://serpapi.com/google-languages
        - pagination: True of False. Enables pagination from all pages. Default 'False'.
        
        Usage:
        
        from google_scholar_py.serpapi_backend.profile_results import SerpApiGoogleScholarProfiles

        parser = SerpApiGoogleScholarProfiles()
        data = parser.scrape_google_scholar_profile_results(
            query='minecraft', 
            api_key='serpapi_api_key', 
            pagination=True,
        )
        
        print(data[0].keys()) # show available keys
        
        for result in data:
            print(result['title'])
            # get other data
        '''
        
        if api_key is None:
            raise Exception('Please enter a SerpApi API key to a `api_key` argument. https://serpapi.com/manage-api-key')
        
        if api_key and query is None:
            raise Exception('Please enter a SerpApi API key to a `api_key`, and a search query to `query` arguments.')
        
        params = {
            'api_key': api_key,                       # serpapi api key: https://serpapi.com/manage-api-key
            'engine': 'google_scholar_profiles',      # serpapi parsing engine
            'mauthors': query,                        # search query
            'hl': lang                                # language
        }
        
        search = GoogleScholarSearch(params) # where data extracts on the backend
        
        if pagination:
            profile_results_data = []
            
            while True:
                results = search.get_dict()  # JSON -> Python dict
                
                if 'error' in results:
                    print(results['error'])
                    break
                
                profile_results_data.append(results['profiles'])
                
                # check for 'next' page
                if 'next' in results.get('pagination', {}):
                    search.params_dict.update(dict(parse_qsl(urlsplit(results['pagination']['next']).query)))
                else:
                    break
                
            # flatten list
            return list(itertools.chain(*profile_results_data))
        else:
            search = GoogleScholarSearch(params)
            results = search.get_dict()
            
            if 'error' in results:
                raise Exception(results['error'])

            return results['profiles']
