# Using custom scripts
# TODO: add SerpApi example usage

from custom_solution.google_scholar_profiles_results import scrape_google_scholar_profiles

data = scrape_google_scholar_profiles(query='blizzard', pagination=False, operating_system='win')

for profile in data:
    print(profile['name'])
    print(profile['interests'])