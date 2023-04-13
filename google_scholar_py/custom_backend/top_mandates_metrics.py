from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selectolax.lexbor import LexborHTMLParser
from typing import List, Dict, Callable
import pandas as pd
import re


class CustomGoogleScholarTopMandates:
    def __init__(self) -> None:
        pass
    

    def parse(self, parser: Callable, top_mandates_data: Callable):
        '''
        Arugments:
        - parser: Callable. Lexbor parser from google_scholar_top_mandates_metrics() function.
        - top_mandates_data: Callable. List to append data to. List origin location is google_scholar_top_mandates_metrics() function. Line 100.
        
        This function parses data from Google Scholar Organic results and appends data to a List.
        
        It's used by google_scholar_top_mandates_metrics().
        
        It returns nothing as it appends data to `top_mandates_data`, 
        which appends it to `top_mandates_data` List in the google_scholar_top_mandates_metrics() function.
        '''
        
        for table in parser.css('tr'):
            try:
                # removes "... - cached"
                # https://regex101.com/r/EfljZp/1
                funder: str = re.sub(r'(\s\s-.*)', '', table.css_first('td.gsc_mlt_t').text()) 
            except: funder = None
            
            try:
                link: str = table.css_first('.gsc_mlt_t a').attrs['href']
            except: link = None
            
            try: 
                two_eighteen: int = table.css_first('td:nth-child(4)').text()
                if '-' in two_eighteen:
                    two_eighteen = None
            except: two_eighteen = None
            
            try: 
                twenty_twenty: str = table.css_first('td:nth-child(5)').text()
                if '-' in twenty_twenty:
                    twenty_twenty = None
            except: twenty_twenty = None
            
            try: 
                twenty_one: str = table.css_first('td:nth-child(6)').text()
                if '-' in twenty_one: # missing % in the table
                    twenty_one = None
            except: twenty_one = None
            
            #TODO: fix selector to extract "overall" data
            # `td:nth-child(6)` is not working also
            # try:
            #     overall: str = table.css('.gsc_mlt_n.gsc_mlt_bd').text()
            # except: overall = None
        
            top_mandates_data.append({
                'funder': funder,
                'link': link,
                '2019': two_eighteen,
                '2020': twenty_twenty,
                '2021': twenty_one,
                # 'overall': overall
            })


    def scrape_top_mandates_metrics(
            self,
            save_to_csv: bool = False, 
            save_to_json: bool = False,
            lang: str = 'en'
        ) -> List[Dict[str, str]]:
        #TODO add argument to support other languages https://serpapi.com/google-languages

        '''
        Results comes from: https://scholar.google.com/citations?view_op=mandates_leaderboard
        
        Returns:
        - funder: str
        - link: str
        - 2019: str
        - 2020: str
        - 2021: str
        - overall: str (not extracted at the moment, selector needs to be fixed)
        
        Arguments: 
        - save_to_csv: True of False. Saves data to CSV file. Default is False. 
        - save_to_json: True of False. Saves data to JSON file. Default is False.
        - lang: str. Language. Defaults to English ('en'). For now, need to be checked yourself. Other languages: https://serpapi.com/google-languages
        
        Usage:
        
        from google_scholar_py import CustomGoogleScholarTopMandates
        
        parser = CustomGoogleScholarTopMandates()
        data = parser.scrape_top_mandates_metrics(
            save_to_csv=True,
            save_to_json=False
        )
        print(json.dumps(data, indent=2))

        for result in data:
            print(result['funder'])
            ...
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
            fix_hairline=True
        )
        
        top_mandates_data: list = []

        driver.get(f'https://scholar.google.com/citations?view_op=mandates_leaderboard&hl={lang}')
        parser = LexborHTMLParser(driver.page_source)
        self.parse(parser=parser, top_mandates_data=top_mandates_data)
        
        if save_to_csv:
            pd.DataFrame(data=top_mandates_data).to_csv('google_scholar_top_mandates_data.csv', 
                                                        index=False, encoding='utf-8')
            
        if save_to_json:
            pd.DataFrame(data=top_mandates_data).to_json('google_scholar_top_mandates_data.json', 
                                                        orient='records')
            
        driver.quit()
        return top_mandates_data
