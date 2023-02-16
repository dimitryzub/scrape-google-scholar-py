from google_scholar_py.custom_backend.author_info_all_articles import CustomGoogleScholarAuthor
from google_scholar_py.custom_backend.organic_search import CustomGoogleScholarOrganic
from google_scholar_py.custom_backend.profiles_results import CustomGoogleScholarProfiles
from google_scholar_py.custom_backend.top_mandates_metrics import CustomGoogleScholarTopMandates
from google_scholar_py.custom_backend.top_publications_metrics import CustomGoogleScholarTopPublications

from google_scholar_py.serpapi_backend.author_results import SerpApiGoogleScholarAuthor
from google_scholar_py.serpapi_backend.profile_results import SerpApiGoogleScholarProfiles
from google_scholar_py.serpapi_backend.organic_results import SerpApiGoogleScholarOrganic
from google_scholar_py.serpapi_backend.organic_cite_results import SerpApiGoogleScholarOrganicCite

import json

parser = CustomGoogleScholarAuthor()
data = parser.scrape_google_scholar_author_data(
    user_id='nHhtvqkAAAAJ',
    operating_system='win',
    parse_articles=True,
    article_pagination=True
)
print(json.dumps(data, indent=2))

parser = CustomGoogleScholarOrganic()
data = parser.scrape_google_scholar_organic_results(
    query='minecraft ss ws',
    operating_system='win',
    pagination=False,
    save_to_csv=True
)
print(json.dumps(data, indent=2))

parser = CustomGoogleScholarProfiles()
data = parser.scrape_google_scholar_profiles(
    query='blizzard',
    operating_system='win',
    pagination=False,
    save_to_csv=False,
    save_to_json=False
)
print(json.dumps(data, indent=2))


parser = CustomGoogleScholarTopMandates()
data = parser.scrape_top_mandates_metrics(
    operating_system='win',
    save_to_csv=True,
    save_to_json=False
)
print(json.dumps(data, indent=2))


parser = CustomGoogleScholarTopPublications()
data = parser.scrape_top_publication_metrics(
    operating_system='win',
    category='bus',
    save_to_csv=True,
    save_to_json=False
)
print(json.dumps(data, indent=2))

# ------------------------SerpApi backend------------------------------

author_parser = SerpApiGoogleScholarAuthor()
data = author_parser.scrape_google_scholar_author_results(
    author_id='nHhtvqkAAAAJ',
    api_key='serpapi_api_key',
    parse_articles=False,
    article_pagination=False
)
print(json.dumps(data, indent=2))


profile_parser = SerpApiGoogleScholarProfiles()
data = profile_parser.scrape_google_scholar_profile_results(
    query='blizzard',
    api_key='serpapi_api_key',
    pagination=False,
)
print(json.dumps(data, indent=2))


organic_parser = SerpApiGoogleScholarOrganic()
data = organic_parser.scrape_google_scholar_organic_results(
    query='minecraft ss ws', 
    api_key='serpapi_api_key', 
    pagination=True
)
print(json.dumps(data, indent=2))

for result in data:
    print(result['title'])

cite_parser = SerpApiGoogleScholarOrganicCite()
data = cite_parser.scrape_google_scholar_cite_results(
    query='minecraft ss ws', 
    api_key='serpapi_api_key', 
    pagination=True
)
print(json.dumps(data, indent=2))

for result in data:
    for citations in result['citations']: 
        print(citations['title']) # or ['snippet'] 