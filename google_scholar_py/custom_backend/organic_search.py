from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selectolax.lexbor import LexborHTMLParser
from typing import List, Dict, Callable
import time, random, re
import pandas as pd
from pathlib import Path


class CustomGoogleScholarOrganic:
    def __init__(self) -> None:
        pass
    

    def parse(self, parser: Callable, organic_results_data: Callable):
        '''
        Arugments:
        - parser:  Lexbor parser from scrape_google_scholar_organic_results() function.
        - organic_results_data: List to append data to. List origin location is scrape_google_scholar_organic_results() function. Line 104.
        
        This function parses data from Google Scholar Organic results and appends data to a List.
        
        It's used by scrape_google_scholar_organic_results().
        
        It returns nothing as it appends data to `organic_results_data`, 
        which appends it to `organic_results_data` List in the scrape_google_scholar_organic_results() function.
        '''
        
        for result in parser.css('.gs_r.gs_or.gs_scl'):
            try:
                title: str = result.css_first('.gs_rt').text()
            except: title = None

            try:
                title_link: str = result.css_first('.gs_rt a').attrs['href']
            except: title_link = None

            try:
                publication_info: str = result.css_first('.gs_a').text()
            except: publication_info = None

            try:
                snippet: str = result.css_first('.gs_rs').text()
            except: snippet = None

            try:
                # if Cited by is present in inline links, it will be extracted
                cited_by_link = ''.join([link.attrs['href'] for link in result.css('.gs_ri .gs_fl a') if 'Cited by' in link.text()])
            except: cited_by_link = None
            
            try:
                # if Cited by is present in inline links, it will be extracted and type cast it to integer
                cited_by_count = int(''.join([re.search(r'\d+', link.text()).group() for link in result.css('.gs_ri .gs_fl a') if 'Cited by' in link.text()]))
            except: cited_by_count = None
            
            try:
                pdf_file: str = result.css_first('.gs_or_ggsm a').attrs['href']
            except: pdf_file = None

            organic_results_data.append({
                'title': title,
                'title_link': title_link,
                'publication_info': publication_info,
                'snippet': snippet if snippet else None,
                'cited_by_link': f'https://scholar.google.com{cited_by_link}' if cited_by_link else None,
                'cited_by_count': cited_by_count if cited_by_count else None,
                'pdf_file': pdf_file
            })

    #TODO: add lang support. https://serpapi.com/google-languages
    def scrape_google_scholar_organic_results(
            self,
            query: str,
            pagination: bool = False,
            save_to_csv: bool = False, 
            save_to_json: bool = False
        ) -> List[Dict[str, str]]:
        '''
        Extracts data from Google Scholar Organic resutls page:
        - title: str
        - title_link: str
        - publication_info: str 
        - snippet: str
        - cited_by_link: str 
        - cited_by_count: int
        - pdf_file: str
        
        Arguments:
        - query: str. Search query. 
        - pagination: bool. Enables or disables pagination. Default is False.
        - save_to_csv: bool. True of False. Default is False.
        - save_to_json: bool. True of False. Default is False.
        
        Usage:
        
        from google_scholar_py import CustomGoogleScholarOrganic

        parser = CustomGoogleScholarOrganic()
        data = parser.scrape_google_scholar_organic_results(
            query='blizzard',
            pagination=False,
            save_to_csv=True
        )
        
        for organic_result in data:
            print(organic_result['title'])
            print(organic_result['pdf_file'])
        '''
        
        # selenium stealth
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        options.add_experimental_option('useAutomationExtension', False) 
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        stealth(driver,
            languages=['en-US', 'en'],
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor='Intel Inc.',
            renderer='Intel Iris OpenGL Engine',
            fix_hairline=True,
        )
        
        page_num = 0
        organic_results_data = []
    
        # parse all pages
        if pagination:
            while True:
                # parse all pages
                driver.get(f'https://scholar.google.com/scholar?q={query}&hl=en&gl=us&start={page_num}')
                parser = LexborHTMLParser(driver.page_source)
                
                self.parse(parser=parser, organic_results_data=organic_results_data)
                
                # pagination
                if parser.css_first('.gs_ico_nav_next'):  # checks for the "Next" page button
                    page_num += 10                        # paginate to the next page
                    time.sleep(random.randint(1, 3))      # sleep between paginations
                else:
                    break
        else:
            # parse first page only
            driver.get(f'https://scholar.google.com/scholar?q={query}&hl=en&gl=us&start={page_num}')
            parser = LexborHTMLParser(driver.page_source)
        
            self.parse(parser=parser, organic_results_data=organic_results_data)
            
        if save_to_csv:
            pd.DataFrame(data=organic_results_data).to_csv('google_scholar_organic_results_data.csv', 
                                                            index=False, encoding='utf-8')
        if save_to_json:
            pd.DataFrame(data=organic_results_data).to_json('google_scholar_organic_results_data.json', 
                                                            orient='records')
        driver.quit()
        
        return organic_results_data
