# each function have documentation with an example "usage" script
from google_scholar_py import CustomGoogleScholarOrganic
from google_scholar_py import SerpApiGoogleScholarOrganic
from google_scholar_py import CustomGoogleScholarTopPublicationCitations

import json

# TODO: add more examples
custom_parser_get_organic_results = CustomGoogleScholarOrganic().scrape_google_scholar_organic_results(
    query='blizzard', 
    pagination=False, 
    save_to_csv=False,
    save_to_json=False
)

top_publication_citation = CustomGoogleScholarTopPublicationCitations().scrape_google_scholar_top_publication_citations(
    journal_publications_link='https://scholar.google.com/citations?hl=en&vq=en&view_op=list_hcore&venue=TdhLrHqKTh8J.2022',
    pagination=True,
    save_to_csv=False,
    save_to_json=False
)

serpapi_parser_get_organic_results = SerpApiGoogleScholarOrganic().scrape_google_scholar_organic_results(
    query='blizzard',
    api_key='your-serpapi-api-key', # https://serpapi.com/manage-api-key
    lang='en',
    pagination=False,
)


print(json.dumps(custom_parser_get_organic_results, indent=2, ensure_ascii=False))
print(json.dumps(serpapi_parser_get_organic_results, indent=2, ensure_ascii=False))
print(json.dumps(top_publication_citation, indent=2, ensure_ascii=False))