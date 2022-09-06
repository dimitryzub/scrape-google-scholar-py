from serpapi import GoogleSearch
import os, json

def serpapi_scrape_articles():
    params = {
        'api_key': os.getenv('API_KEY'),        # your serpapi api key
        'engine': 'google_scholar_author',      # serpapi parsing engine
        'hl': 'en',                             # language of the search
        'author_id': '_xwYD2sAAAAJ',            # author ID
        'start': '0',                           # page number: 0 - first, 1 second and so on.
        'num': '100'                            # number of articles per page
    }

    search = GoogleScholarSearch(params)

    all_articles = []

    while True:
        results = search.get_dict()

        for article in results['articles']:
            title = article.get('title')
            link = article.get('link')
            authors = article.get('authors')
            publication = article.get('publication')
            citation_id = article.get('citation_id')
            year = article.get('year')
            cited_by_count = article.get('cited_by').get('value')

            all_articles.append({
                'title': title,
                'link': link,
                'authors': authors,
                'publication': publication,
                'citation_id': citation_id,
                'cited_by_count': cited_by_count,
                'year': year
            })
        
        # check if the next page is present in 'serpapi_pagination' dict key
        if 'next' in results.get('serpapi_pagination', {}):
            # split URL in parts as a dict() and update 'search' variable to a new page
            search.params_dict.update(dict(parse_qsl(urlsplit(results['serpapi_pagination']['next']).query)))
        else:
            break

    print(json.dumps(all_articles, indent=2, ensure_ascii=False))
