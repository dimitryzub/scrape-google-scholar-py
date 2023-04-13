from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selectolax.lexbor import LexborHTMLParser
from typing import List, Dict, Callable, Union
import pandas as pd

class CustomGoogleScholarTopPublications:
    def __init__(self) -> None:
        pass


    def parse(self, parser: Callable, top_publications_data: Callable):
        '''
        Arugments:
        - parser: Callable. Lexbor parser from google_scholar_top_publication_metrics() function.
        - top_publications_data: Callable. List to append data to. List origin location is google_scholar_top_publication_metrics() function. Line 100.
        
        This function parses data from Google Scholar Organic results and appends data to a List.
        
        It's used by google_scholar_top_publication_metrics().
        
        It returns nothing as it appends data to `top_publications_data`, 
        which appends it to `top_publications_data` List in the google_scholar_top_publication_metrics() function.
        '''

        # selectors skips table header row
        for table in parser.css('tr:not(:first-child)'):
            try:
                title: str = table.css_first('td.gsc_mvt_t').text()
            except: title = None
            
            try: 
                h5_index: int = table.css_first('a.gs_ibl').text()
            except: h5_index = None
            
            try: 
                h5_index_link: str = f"https://scholar.google.com{table.css_first('a.gs_ibl').attrs['href']}"
            except: h5_index_link = None
            
            try: 
                h5_median: int = table.css_first('span.gs_ibl').text()
            except: h5_median = None
        
            top_publications_data.append({
                'title': title,
                'h5_index': int(h5_index) if h5_index else h5_index,
                'h5_index_link': h5_index_link,
                'h5_median': int(h5_median) if h5_median else h5_median
            })


    def scrape_top_publication_metrics(
            self,
            category: str = '', 
            lang: str = 'en',
            save_to_csv: bool = False, 
            save_to_json: bool = False,
        ) -> List[Dict[str, Union[str, int]]]:
        #TODO add subcategories to subcategory arg
        #TODO: support other languages: lang='spanish' -> 'sp'. https://serpapi.com/google-languages


        '''
        Results comes from: https://scholar.google.com/citations?view_op=top_venues
        
        Returns:
        - title: str
        - h5_index: int
        - h5_index_link: str
        - h5_median: int
        
        Arguments: 
        - save_to_csv: True of False. Default is False. Saves data to CSV file.
        - save_to_json: True of False. Default is False. Saves data to JSON file.
        - lang: str. Language. Defaults to English ('en'). For now, need to be checked yourself. Other languages: https://serpapi.com/google-languages
        - category: str. Available categories showed in the function documentation below.
            Available categories:
            - "bus": Business, Economics & Management
            - "chm": Chemical & Material Sciences
            - "eng": Engineering & Computer Science
            - "med": Health & Medical Sciences
            - "hum": Humanities, Literature & Arts
            - "bio": Life Sciences & Earth Sciences
            - "phy": Physics & Mathematics
            - "soc": Social Sciences
            
        Usage:
        
        from google_scholar_py import CustomGoogleScholarTopPublications
        
        data = CustomGoogleScholarTopPublications().scrape_top_publication_metrics(category='eng', lang='en') # sv = swedish
        
        for result in data:
            print(result['title'])
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
        
        top_publications_data = []

        if category:
            driver.get(f'https://scholar.google.com/citations?view_op=top_venues&hl={lang}&vq={category}')
            parser = LexborHTMLParser(driver.page_source)
            self.parse(parser=parser, top_publications_data=top_publications_data)
        else: 
            # no vq={category} URL parameter
            driver.get(f'https://scholar.google.com/citations?view_op=top_venues&hl={lang}&vq={category}') # vq='' which will redirect to the page with no applied category
            parser = LexborHTMLParser(driver.page_source)
            self.parse(parser=parser, top_publications_data=top_publications_data)
            
        if save_to_csv:
            pd.DataFrame(data=top_publications_data).to_csv('google_scholar_top_publications_data.csv', 
                                                            index=False, encoding='utf-8')
        if save_to_json:
            pd.DataFrame(data=top_publications_data).to_json('google_scholar_top_publications_data.json', 
                                                            orient='records')
            
        driver.quit()
        return top_publications_data
