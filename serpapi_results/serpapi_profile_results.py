from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import os, json


def serpapi_scrape_all_authors():
    params = {
        'api_key': os.getenv('API_KEY'),      # SerpApi API key
        'engine': 'google_scholar_profiles',  # profile results search engine
        'mauthors': 'blizzard',               # search query
    }
    search = GoogleSearch(params)

    profile_results_data = []

    profiles_is_present = True
    while profiles_is_present:

        profile_results = search.get_dict()

        for profile in profile_results['profiles']:

            print(f'Currently extracting {profile["name"]} with {profile["author_id"]} ID.')

            thumbnail = profile['thumbnail']
            name = profile['name']
            link = profile['link']
            author_id = profile['author_id']
            affiliations = profile['affiliations']
            email = profile.get('email')
            cited_by = profile.get('cited_by')
            interests = profile.get('interests')

            profile_results_data.append({
                'thumbnail': thumbnail,
                'name': name,
                'link': link,
                'author_id': author_id,
                'email': email,
                'affiliations': affiliations,
                'cited_by': cited_by,
                'interests': interests
            })

            if 'next' in profile_results['pagination']:
                # split URL in parts as a dict() and update search 'params' variable to a new page
                search.params_dict.update(dict(parse_qsl(urlsplit(profile_results['pagination']['next']).query)))
            else:
                profiles_is_present = False

    return profile_results_data
