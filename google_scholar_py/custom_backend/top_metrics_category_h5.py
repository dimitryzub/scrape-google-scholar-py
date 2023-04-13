from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selectolax.lexbor import LexborHTMLParser
from typing import List, Dict, Callable
import pandas as pd
import re


class CustomCategoryArticles:
    def __init__(self) -> None:
        pass

    
    def parse(self, parser: Callable, category_articles: Callable):
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
            title = table.css_first('.gsc_mp_anchor_lrge').text()
            title_link = table.css_first('a.gsc_mp_anchor_lrge').attrs['href']
            
            authors = table.css_first('.gsc_mpat_ttl+ .gs_gray').text()
            citation = table.css_first('.gs_gray+ .gs_gray').text()
            
            citation_journal = re.search(r'', citation).group()
            citation_volume = re.search(r'', citation).group()
            citation_issue_number = re.search(r'', citation).group()
            citation_pages = re.search(r'', citation).group()
            
            
            cited_by = table.css_first('.gsc_mpat_c .gsc_mp_anchor').text()
            cited_by_link = table.css_first('.gsc_mpat_c .gsc_mp_anchor').attrs['href']
            year = table.css_first('.gsc_mp_anchor.gs_nph').text()

            
            category_articles.append({
                'title': title,
                'title_link': title_link,
                'authors': authors,
                'citation': {
                  'citation_journal': citation_journal,  
                  'citation_volume': citation_volume,  
                  'citation_issue_number': citation_issue_number,  
                  'citation_pages': citation_pages,
                },
                'cited_by': cited_by,
                'cited_by_link': cited_by_link,
                'year': year,
            })
            
    def scrape_category_articles(
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
        
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
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
        
        category_articles = []

        driver.get(f'https://scholar.google.com/citations?view_op=mandates_leaderboard&hl={lang}')
        parser = LexborHTMLParser(driver.page_source)
        self.parse(parser=parser, category_articles=category_articles)
        
        if save_to_csv:
            pd.DataFrame(data=category_articles).to_csv('google_scholar_top_mandates_category_articles_data.csv', 
                                                        index=False, encoding='utf-8')
            
        if save_to_json:
            pd.DataFrame(data=category_articles).to_json('google_scholar_top_mandates_category_articles_data.json', 
                                                        orient='records')
            
        driver.quit()
        return category_articles
