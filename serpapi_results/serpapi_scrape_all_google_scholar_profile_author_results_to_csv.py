# blog post: https://serpapi.com/blog/scrape-all-google-scholar-profile-author-results-with-python-and-serpapi/

import os, json
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl
import pandas as pd


def profile_results():
    print('Extracting profile results..')

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

        for profile in profile_results.get('profiles', []):

            print(f'Currently extracting {profile.get("name")} with {profile.get("author_id")} ID.')

            thumbnail = profile.get('thumbnail')
            name = profile.get('name')
            link = profile.get('link')
            author_id = profile.get('author_id')
            affiliations = profile.get('affiliations')
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

        if 'next' in profile_results.get('pagination', {}):
            search.params_dict.update(dict(parse_qsl(urlsplit(profile_results.get('pagination').get('next')).query)))
        else:
            profiles_is_present = False

    return profile_results_data


def author_results():
    print('extracting author results..')

    author_results_data = []

    for author_id in profile_results():
        print(f"Parsing {author_id['author_id']} author ID.")

        params = {
            'api_key': os.getenv('API_KEY'),      # SerpApi API key
            'engine': 'google_scholar_author',    # author results search engine
            'author_id': author_id['author_id'],  # search query
            'hl': 'en'
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        thumbnail = results.get('author').get('thumbnail')
        name = results.get('author').get('name')
        affiliations = results.get('author').get('affiliations')
        email = results.get('author').get('email')
        website = results.get('author').get('website')
        interests = results.get('author').get('interests')

        cited_by_table = results.get('cited_by', {}).get('table')
        cited_by_graph = results.get('cited_by', {}).get('graph')

        public_access_link = results.get('public_access', {}).get('link')
        available_public_access = results.get('public_access', {}).get('available')
        not_available_public_access = results.get('public_access', {}).get('not_available')
        co_authors = results.get('co_authors')

        author_results_data.append({
            'thumbnail': thumbnail,
            'name': name,
            'affiliations': affiliations,
            'email': email,
            'website': website,
            'interests': interests,
            'cited_by_table': cited_by_table,
            'cited_by_graph': cited_by_graph,
            'public_access_link': public_access_link,
            'available_public_access': available_public_access,
            'not_available_public_access': not_available_public_access,
            'co_authors': co_authors
        })

    return author_results_data


def all_author_articles():
    author_article_results_data = []

    for index, author_id in enumerate(profile_results(), start=1):
        print(f"Parsing author #{index} with {author_id['author_id']} author ID.")

        params = {
            'api_key': os.getenv('API_KEY'),     # SerpApi API key
            'engine': 'google_scholar_author',   # author results search engine
            'hl': 'en',                          # language
            'sort': 'pubdate',                   # sort by year
            'author_id': author_id['author_id']  # search query
        }
        search = GoogleSearch(params)

        articles_is_present = True
        while articles_is_present:
            results = search.get_dict()

            for article in results.get('articles', []):
                title = article.get('title')
                link = article.get('link')
                citation_id = article.get('citation_id')
                authors = article.get('authors')
                publication = article.get('publication')
                cited_by_value = article.get('cited_by', {}).get('value')
                cited_by_link = article.get('cited_by', {}).get('link')
                cited_by_cites_id = article.get('cited_by', {}).get('cites_id')
                year = article.get('year')

                author_article_results_data.append({
                    'article_title': title,
                    'article_link': link,
                    'article_year': year,
                    'article_citation_id': citation_id,
                    'article_authors': authors,
                    'article_publication': publication,
                    'article_cited_by_value': cited_by_value,
                    'article_cited_by_link': cited_by_link,
                    'article_cited_by_cites_id': cited_by_cites_id,
                })

            if 'next' in results.get('serpapi_pagination', []):
                search.params_dict.update(dict(parse_qsl(urlsplit(results.get('serpapi_pagination').get('next')).query)))
            else:
                articles_is_present = False

    return author_article_results_data


def save_author_result_to_csv():
    print('Waiting for author results to save..')
    pd.DataFrame(data=profile_results()).to_csv('google_scholar_author_results.csv', encoding='utf-8', index=False)

    print('Author Results Saved.')


def save_author_articles_to_csv():
    print('Waiting for author articles to save..')
    pd.DataFrame(data=profile_results()).to_csv('google_scholar_author_articles.csv', encoding='utf-8', index=False)

    print('Author Articles Saved.')


def save_profile_results_to_csv():
    print('Waiting for profile results to save..')
    pd.DataFrame(data=profile_results()).to_csv('google_scholar_profile_results.csv', encoding='utf-8', index=False)

    print('Profile Results Saved.')
