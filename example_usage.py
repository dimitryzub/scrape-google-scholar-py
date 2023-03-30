# each function have documentation with an example "usage" script
from google_scholar_py import CustomGoogleScholarOrganic
from google_scholar_py import SerpApiGoogleScholarOrganic
import json

# TODO: add more examples
custom_parser = CustomGoogleScholarOrganic().scrape_google_scholar_organic_results(
    query='blizzard', 
    pagination=False, 
    save_to_csv=False,
    save_to_json=False
)

serpapi_parser = SerpApiGoogleScholarOrganic().scrape_google_scholar_organic_results(
    query='blizzard',
    api_key='your-serpapi-api-key', # https://serpapi.com/manage-api-key
    lang='en',
    pagination=False,
)

print(json.dumps(custom_parser, indent=2))
print(json.dumps(serpapi_parser, indent=2))
