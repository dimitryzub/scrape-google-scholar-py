from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selectolax.lexbor import LexborHTMLParser
from typing import List, Dict, Callable, Union
import pandas as pd
import time, random

class CustomGoogleScholarTopPublicationArticle:
    def __init__(self) -> None:
        pass
    

    def parse(self, parser: Callable, publication_citation_data: Callable):
        '''
        Arugments:
        - parser:  Lexbor parser from scrape_google_scholar_top_publication_articles() function.
        - publication_citation_data: List to append data to. List origin location is scrape_google_scholar_top_publication_articles() function. Line 104.
        
        This function parses data from Google Scholar Organic results and appends data to a List.
        
        It's used by scrape_google_scholar_top_publication_articles().
        '''
        
        # selects the whole table without the first row (header row) 
        for result in parser.css('tr:not(:first-child)'):
            try:
                title: str = result.css_first('.gsc_mp_anchor_lrge').text()
            except: title = None

            try:
                title_link: str = f"https://scholar.google.com{result.css_first('a.gsc_mp_anchor_lrge').attrs['href']}"
            except: title_link = None

            try:
                authors: list = result.css_first('.gsc_mpat_ttl+ .gs_gray').text().split(', ')
            except: authors = None
            
            try:
                published_at: str = result.css_first('.gs_gray+ .gs_gray').text()
            except: published_at = None
            
            try:
                cited_by_count: int = int(result.css_first('.gsc_mpat_c .gsc_mp_anchor').text())
            except: cited_by_count = None

            try:
                cited_by_link: str = f"https://scholar.google.com{result.css_first('.gsc_mpat_c a.gsc_mp_anchor').attrs['href']}"
            except: cited_by_link = None
            
            try:
                year: int = int(result.css_first('.gsc_mp_anchor.gs_nph').text())
            except: year = None
            
            
            publication_citation_data.append({
                'title': title,
                'title_link': title_link,
                'authors': authors,
                'cited_by_link': cited_by_link,
                'cited_by_count': cited_by_count,
                'year': year,
                'published_at': published_at
            })

    #TODO: add lang support. https://serpapi.com/google-languages
    def scrape_google_scholar_top_publication_articles(
            self,
            journal_publications_link: str,
            pagination: bool = False,
            save_to_csv: bool = False, 
            save_to_json: bool = False
        ) -> List[Dict[str, Union[str, List[str], int]]]:
        '''
        Results comes from (for example): https://scholar.google.com/citations?hl=en&vq=en&view_op=list_hcore&venue=9oNLl9DgMnQJ.2022
        
        Extracts data from Google Scholar Top Publication Metrics Citation page:
        - title: str
        - title_link: str
        - authors: list 
        - cited_by_count: int
        - cited_by_link: str 
        - year: int
        - published_at: str
    
        Arguments:
        - journal_publications_link: str. Search query. 
        - pagination: bool. Enables or disables pagination. Default is False.
        - save_to_csv: bool. True of False. Default is False.
        - save_to_json: bool. True of False. Default is False.
        
        Usage:
        
        from google_scholar_py import CustomGoogleScholarTopPublicationArticle

        parser = CustomGoogleScholarTopPublicationArticle()
        data = parser.scrape_google_scholar_top_publication_articles(
            journal_publications_link='https://scholar.google.com/citations?hl=en&vq=en&view_op=list_hcore&venue=9oNLl9DgMnQJ.2022', # or link variable that stores the link
            pagination=False,
            save_to_csv=True
        )
        
        for citations in data:
            print(citations['title'], citations['year'], citations['published_at'], sep='\\n')
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
        publication_citation_data = []
    
        # parse all pages
        if pagination:
            while True:
                driver.get(journal_publications_link + f'&cstart={page_num}') # 'cstart' paramter is for pagination
                parser = LexborHTMLParser(driver.page_source)
                
                self.parse(parser=parser, publication_citation_data=publication_citation_data)
                
                # pagination
                if parser.css_first('.gsc_pgn_pnx:not([disabled])'):  # checks if the "Next" page button selector is not disabled
                    page_num += 20                                    # paginate to the next page
                    time.sleep(random.randint(1, 3))                  # sleep between paginations
                else:
                    break
        else:
            # parse first page only
            driver.get(journal_publications_link)
            parser = LexborHTMLParser(driver.page_source)
        
            self.parse(parser=parser, publication_citation_data=publication_citation_data)
            
        if save_to_csv:
            pd.DataFrame(data=publication_citation_data).to_csv('google_scholar_top_publication_citations.csv', 
                                                            index=False, encoding='utf-8')
        if save_to_json:
            pd.DataFrame(data=publication_citation_data).to_json('google_scholar_top_publication_citations.json', 
                                                            orient='records')
        driver.quit()
        
        return publication_citation_data
