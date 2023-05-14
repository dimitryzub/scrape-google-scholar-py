import pytest
import unittest
from pathlib import Path
import os
from google_scholar_py.custom_backend.profiles_results import CustomGoogleScholarProfiles


# # Tests for CustomGoogleScholarProfiles class
# @pytest.fixture(scope='session')
# def google_scholar_parser():
#     return CustomGoogleScholarProfiles()

@pytest.fixture(scope='session')
def search_query():
    return 'blizzard'

def test_custom_google_scholar_profiles_scrape_without_pagination(search_query):
    results = CustomGoogleScholarProfiles().scrape_google_scholar_profiles(query=search_query, pagination=False)
    assert len(results) > 0

def test_custom_google_scholar_profiles_scrape_with_pagination(search_query):
    results = CustomGoogleScholarProfiles().scrape_google_scholar_profiles(query=search_query, pagination=True)
    assert len(results) > 0

def test_custom_google_scholar_profiles_save_to_csv(search_query):
    CustomGoogleScholarProfiles().scrape_google_scholar_profiles(query=search_query, pagination=False, save_to_csv=True)
    
    # ../ as file saves in root, might save to a special "results" folder
    assert Path().cwd().joinpath('tests', '../google_scholar_profile_results_data.csv').exists()

def test_custom_google_scholar_profiles_save_to_json(search_query):
    CustomGoogleScholarProfiles().scrape_google_scholar_profiles(query=search_query, pagination=False, save_to_json=True)
    
    # # ../ as file saves in root, might save to a special "results" folder
    assert Path().cwd().joinpath('tests', '../google_scholar_profile_results_data.json').exists()
    
# @pytest.fixture(scope='session')
# def remove_test_files():    
#     csv_file = Path().cwd().parent / 'google_scholar_profile_results_data.csv'
#     json_file = Path().cwd().parent / 'google_scholar_profile_results_data.json'
#     os.remove(csv_file)
#     os.remove(json_file)
    

# Tests for scrape_google_scholar_profiles function
class TestScrapeGoogleScholarProfiles(unittest.TestCase):

    def test_scrape_google_scholar_profiles_returns_list(self):
        query = "machine learning"
        results = CustomGoogleScholarProfiles().scrape_google_scholar_profiles(query)
        self.assertIsInstance(results, list)

    def test_scrape_google_scholar_profiles_returns_correct_data_types(self):
        query = "machine learning"
        results = CustomGoogleScholarProfiles().scrape_google_scholar_profiles(query)
        
        for profile_data in results:
            self.assertIsInstance(profile_data, dict)
            self.assertIsInstance(profile_data['name'], str)
            self.assertIsInstance(profile_data['link'], str)
            self.assertIsInstance(profile_data['affiliations'], str)
            self.assertIsInstance(profile_data['email'], str)
            self.assertIsInstance(profile_data['cited_by_count'], int or None)
            self.assertIsInstance(profile_data['interests'], list or None)
            for interest in profile_data['interests']:
                self.assertIsInstance(interest, str)

    def test_scrape_google_scholar_profiles_returns_valid_data(self):
        query = "machine learning"
        results = CustomGoogleScholarProfiles().scrape_google_scholar_profiles(query=query)
        
        for profile_data in results:
            self.assertIsNotNone(profile_data['name'])
            self.assertIsNotNone(profile_data['link'])
            self.assertIsNotNone(profile_data['affiliations'])
            self.assertIsNotNone(profile_data['email'])
            self.assertIsNotNone(profile_data['cited_by_count'])
            self.assertGreater(len(profile_data['interests']), 0)
            
    

if __name__ == '__main__':
    unittest.main()