from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selectolax.lexbor import LexborHTMLParser
from typing import List, Union, Dict
from pathlib import Path


class CustomGoogleScholarAuthor:
    def __init__(self) -> None:
        pass


    def scrape_google_scholar_author_data(
            self,
            user_id: str, 
            parse_articles: bool = False,
            article_pagination: bool = False 
        ) -> Dict[str, List[Union[str, int, None]]]:
        '''
        Extracts data from Google Scholar Author profile page:
        - Info about the author itself
        - Co-authors: name, link, affiliation
        - Author: title, link, authors, publication, cited by, year.
        - Articles: first 100 if pagination is False, or all if pagination is True. 

        Arguments:
        - user_id: str. User ID from Google Scholar profile located in the URL.
        - parse_articles: True of False. If True, extracts first 100 articles. Default False.
        - article_pagination: True of False. If True, extracts beyond first 100 articles. 

        Usage:
        
        from google_scholar_py import CustomGoogleScholarAuthor
        
        parser = CustomGoogleScholarAuthor()
        data = parser.scrape_google_scholar_author_data(
            user_id='nHhtvqkAAAAJ',
            parse_articles=True,
            article_pagination=True
        )
        print(json.dumps(data, indent=2))
        
        print(data['info']) # author info
        print(data['co-authors'])

        for article in data['articles']:
            print(article['title'])
            print(article['cited_by_count'])
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
            fix_hairline=True,
        )
        
        driver.get(f'https://scholar.google.com/citations?user={user_id}&hl=en&gl=us&pagesize=100')
        parser = LexborHTMLParser(driver.page_source)
        
        profile_info = {
            'info': {},
            'co-authors': [], 
            'articles': [][:-1] # [:-1] to not to return the last None element. Weird approach, I know. Revisit in the future.
        }
        
        profile_info['info']['name'] = parser.css_first('#gsc_prf_in').text()
        profile_info['info']['affiliations'] = parser.css_first('.gsc_prf_ila').text()
        profile_info['info']['email'] = parser.css_first('#gsc_prf_ivh').text()
        profile_info['info']['interests'] = [interest.text() for interest in parser.css('#gsc_prf_int .gs_ibl')]
        
        for co_author in parser.css('.gsc_rsb_aa'):
            profile_info['co-authors'].append({
                'name': co_author.css_first('.gsc_rsb_a_desc a').text(),
                'profile_link': f"https://scholar.google.com{co_author.css_first('.gsc_rsb_a_desc a').attrs['href']}",
                'affiliation': co_author.css_first('.gsc_rsb_a_ext').text(),
            })
            
        # extracts only first 100 articles, WITHOUT paginaiton
        if parse_articles:
            # TODO: make a separate function to extract articles
            for index, article in enumerate(parser.css('.gsc_a_tr'), start=1):
                try:
                    article_title = article.css_first('.gsc_a_at').text()
                except: article_title = None
                
                try: 
                    article_link = f"https://scholar.google.com{article.css_first('.gsc_a_at').attrs['href']}"
                except: article_link = None
                
                try:
                    if ',' in article.css_first('.gsc_a_at+ .gs_gray').text():
                        article_authors: List[str] = article.css_first('.gsc_a_at+ .gs_gray').text().split(', ') # list of authors
                    else: article_authors = article.css_first('.gsc_a_at+ .gs_gray').text()           # single authour
                except: article_authors = None
                
                try:
                    article_publication = article.css_first('.gs_gray+ .gs_gray').text()
                except: article_publication = None

                try:
                    cited_by_count = article.css_first('.gsc_a_ac').text() 
                except: cited_by_count = None
                
                try: 
                    publication_year = article.css_first('.gsc_a_hc').text()
                except: publication_year = None

                profile_info['articles'].append({
                    'title': article_title,
                    'link': article_link,
                    'authors': article_authors,
                    'publication': article_publication if article_publication else None,
                    'publication_year': int(publication_year) if publication_year else publication_year or None, # int value or None or empty str
                    'cited_by_count': int(cited_by_count) if cited_by_count else cited_by_count or None # int value or None or empty str
                }) 
        elif parse_articles is False:
            profile_info.pop('articles')

        page_num = 0

        # extracts all articles
        if parse_articles and article_pagination:
            while True:
                driver.get(f'https://scholar.google.com/citations?user={user_id}&hl=en&gl=us&cstart={page_num}&pagesize=100')
                parser = LexborHTMLParser(driver.page_source)
                
                for article in parser.css('.gsc_a_tr'):
                    try:
                        article_title = article.css_first('.gsc_a_at').text()
                    except: article_title = None
                    
                    try: 
                        article_link = f"https://scholar.google.com{article.css_first('.gsc_a_at').attrs['href']}"
                    except: article_link = None
                    
                    try:
                        if ',' in article.css_first('.gsc_a_at+ .gs_gray').text():
                            article_authors: List[str] = article.css_first('.gsc_a_at+ .gs_gray').text().split(', ') # list of authors
                        else: article_authors = article.css_first('.gsc_a_at+ .gs_gray').text()           # single authour
                    except: article_authors = None
                    
                    try:
                        article_publication = article.css_first('.gs_gray+ .gs_gray').text()
                    except: article_publication = None

                    try:
                        cited_by_count = article.css_first('.gsc_a_ac').text() 
                    except: cited_by_count = None
                    
                    try: 
                        publication_year = article.css_first('.gsc_a_hc').text()
                    except: publication_year = None

                    profile_info['articles'].append({
                        'title': article_title,
                        'link': article_link,
                        'authors': article_authors,
                        'publication': article_publication if article_publication else None,
                        'publication_year': int(publication_year) if publication_year else publication_year or None, # int value or None or empty str
                        'cited_by_count': int(cited_by_count) if cited_by_count else cited_by_count or None # int value or None or empty str
                    })

                if parser.css_first('.gsc_a_e'):
                    break
                else:
                    page_num += 100  # paginate to the next page
                    
        # remove articles key if user don't want to extract it
        elif article_pagination and parse_articles is False: 
            profile_info.pop('articles')
            
        return profile_info
