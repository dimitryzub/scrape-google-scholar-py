from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selectolax.lexbor import LexborHTMLParser
from typing import List, Dict, Callable
import time, random, re
import pandas as pd


class CustomGoogleScholarProfiles:
    def __init__(self) -> None:
        pass
    

    def parse(self, parser: Callable, profile_results_data: Callable):
        '''
        Arugments:
        - parser: Callable. Lexbor parser from scrape_google_scholar_profiles() function.
        - profile_results_data: Callable. List to append data to. List origin location is scrape_google_scholar_profiles() function. Line 100.
        
        This function parses data from Google Scholar Organic results and appends data to a List.
        
        It's used by scrape_google_scholar_profiles().
        
        It returns nothing as it appends data to `profile_results_data`, 
        which appends it to `profile_results_data` List in the scrape_google_scholar_profiles() function.
        '''
        
        for profile in parser.css('.gs_ai_chpr'):
            try:
                name: str = profile.css_first('.gs_ai_name a').text()
            except: name = None
            
            try:
                link: str = f'https://scholar.google.com{profile.css_first(".gs_ai_name a").attrs["href"]}'
            except: link = None
            
            try:
                affiliations: str = profile.css_first('.gs_ai_aff').text()
            except: affiliations = None
            
            try:
                interests: list = [interest.text() for interest in profile.css('.gs_ai_one_int')]
            except: interests = None
            
            try:
                email: str = profile.css_first('.gs_ai_eml').text()
            except: email = None
            
            try:
                cited_by: int = re.search(r'\d+', profile.css_first('.gs_ai_cby').text()).group() # Cited by 17143 -> 17143
            except: cited_by = None

            profile_results_data.append({
                'name': name,
                'link': link,
                'affiliations': affiliations,
                'interests': interests if interests else None,
                'email': email if email else None,
                'cited_by_count': int(cited_by) if cited_by else None
            })


    def scrape_google_scholar_profiles(
            self, 
            query: str, 
            pagination: bool = False, 
            operating_system: str = 'Windows' or 'Linux',
            save_to_csv: bool = False, 
            save_to_json: bool = False
        ) -> List[Dict[str, str]]:
        '''
        Extracts data from Google Scholar Organic Profile resutls page:
        - name: str
        - link: str
        - affiliations: str 
        - email: str
        - cited_by_count: int
        
        Arguments:
        - query: str. Search query. 
        - pagination: bool. Enables or disables pagination. Default is False.
        - operating_system: str. 'Windows' or 'Linux', Checks for operating system to either run Windows or Linux verson of chromedriver
        - save_to_csv: bool. True of False. Default is False.
        - save_to_json: bool. True of False. Default is False.
        
        Usage:
        
        from google_scholar_py.custom_backend.profiles_results import CustomGoogleScholarProfiles
        
        parser = CustomGoogleScholarProfiles()
        data = parser.scrape_google_scholar_profiles(
            query='blizzard',
            operating_system='win',
            pagination=False,
            save_to_csv=True
        )
        print(json.dumps(data, indent=2))
        
        data = scrape_google_scholar_profiles(query='blizzard', pagination=False, operating_system='win') # pagination defaults to False 
        
        for profile_results in data:
            print(profile_results['name'])
            print(profile_results['email'])
        '''
        
        # selenium stealth
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # checks for operating system to either run Windows or Linux verson of chromedriver
        # expects to have chromedriver near the runnable file
        if operating_system is None:
            raise Exception('Please provide your OS to `operating_system` argument: "Windows" or "Linux" for script to operate.')
        
        if operating_system.lower() == 'windows' or 'win':
            driver = webdriver.Chrome(options=options, service=Service(executable_path='chromedriver.exe'))
        elif operating_system.lower() == 'linux': 
            driver = webdriver.Chrome(options=options, service=Service(executable_path='chromedriver'))
        
        stealth(driver,
            languages=['en-US', 'en'],
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor='Intel Inc.',
            renderer='Intel Iris OpenGL Engine',
            fix_hairline=True
        )
        
        params = {} # stores next page token to add to URL later
        page_num = 0
        profile_results_data = []

        if pagination:
            while True:
                # if next page token appears, add to to URL as URL parameter
                # otherwise, do a search without next page token parameter (Line: 101)
                if params.get('after_author') is None:
                    driver.get(f'https://scholar.google.com/citations?view_op=search_authors&mauthors={query}&hl=en&astart={page_num}')
                    parser = LexborHTMLParser(driver.page_source)
                    
                    #TODO: replace parsel with selectolax completely
                    selector = Selector(text=driver.page_source)  # to check next page token
                
                    self.parse(parser=parser, profile_results_data=profile_results_data)
                    
                    # check if the next arrow button is active by checking 'onclick' attribute
                    if selector.css('.gsc_pgn button.gs_btnPR::attr(onclick)').get():
                        # extracting next page token and passing to 'after_author' query URL parameter
                        params['after_author'] = re.search(r'after_author\\x3d(.*)\\x26', str(selector.css('.gsc_pgn button.gs_btnPR::attr(onclick)').get())).group(1) # -> XB0HAMS9__8J
                        page_num += 10                        # paginate to the next page
                        time.sleep(random.randint(1, 3))      # sleep between paginations
                    else:
                        break
                else:
                    driver.get(f'https://scholar.google.com/citations?view_op=search_authors&mauthors={query}&hl=en&astart={page_num}&after_author={params["after_author"]}')
                    parser = LexborHTMLParser(driver.page_source)
                    
                    #TODO: replace parsel with selectolax completely
                    selector = Selector(text=driver.page_source) # to check next page token
                
                    self.parse(parser=parser, profile_results_data=profile_results_data)
                    
                    if selector.css('.gsc_pgn button.gs_btnPR::attr(onclick)').get():
                        # extracting next page token and passing to 'after_author' query URL parameter
                        params['after_author'] = re.search(r'after_author\\x3d(.*)\\x26', str(selector.css('.gsc_pgn button.gs_btnPR::attr(onclick)').get())).group(1) # -> XB0HAMS9__8J
                        page_num += 10                        # paginate to the next page
                        time.sleep(random.randint(1, 3))      # sleep between paginations
                    else:
                        break
        else:
            # parse single, first page
            driver.get(f'https://scholar.google.com/citations?view_op=search_authors&mauthors={query}&hl=en&astart={page_num}')
            parser = LexborHTMLParser(driver.page_source)
        
            self.parse(parser=parser, profile_results_data=profile_results_data)

        driver.quit()
        
        if save_to_csv:
            pd.DataFrame(data=profile_results_data).to_csv('google_scholar_profile_results_data.csv', 
                                                            index=False, encoding='utf-8')
        if save_to_json:
            pd.DataFrame(data=profile_results_data).to_json('google_scholar_profile_results_data.json', 
                                                            orient='records')
        
        return profile_results_data       
