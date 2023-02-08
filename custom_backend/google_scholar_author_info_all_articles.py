from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from selectolax.lexbor import LexborHTMLParser
from typing import List, Union, Dict


def scrape_google_scholar_author_data(user_id: str, 
                                      operating_system: str = 'Windows' or 'Linux',
                                      ) -> Dict[str, List[Union[str, int, None]]]:
    '''
    Extracts data from Google Scholar Author profile page:
    - Info about the author itself
    - Co-authors: name, link, affiliation
    - Author articles (pagination is enabled by default and can't be disabled ATM): title, link, authors, publication, cited by, year 

    Returns Dict of Dicts and two Lists.
    
    Arguments:
    - user_id: str. User ID from Google Scholar profile located in the URL.
    - operating_system: str. 'Windows' (or 'win') or 'Linux', Checks for operating system to either run Windows or Linux verson of chromedriver

    __________________________________________
    Example usage when calling this function:
    
    data = scrape_google_scholar_author_data()
    
    data['info'] # author info
    data['co-authors']
    
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
    
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    # checks for operating system to either run Windows or Linux verson of chromedriver
    # expects to have chromedriver near the runnable file
    if operating_system is None:
        raise Exception('Please provide your OS to `operating_system` argument: "Windows" or "Linux" for script to operate.')
    
    if operating_system.lower() == 'windows' or 'win':
        driver = webdriver.Chrome(options=options, service=Service(executable_path='chromedriver.exe'))
    
    if operating_system.lower() == 'linux': 
        driver = webdriver.Chrome(options=options, service=Service(executable_path='chromedriver'))
    
    stealth(driver,
        languages=['en-US', 'en'],
        vendor='Google Inc.',
        platform='Win32',
        webgl_vendor='Intel Inc.',
        renderer='Intel Iris OpenGL Engine',
        fix_hairline=True,
    )
    
    driver.get(f'https://scholar.google.com/citations?user={user_id}&hl=en&gl=us')
    parser = LexborHTMLParser(driver.page_source)
    
    profile_info: Dict[str, Union[Dict, List]] = {
        'info': {},
        'co-authors': [], 
        'articles': [][:-1] # [:-1] to not to return the last None element. Weird approach, I know. Revisit in the future.
    }
    
    profile_info['info']['name']: str = parser.css_first('#gsc_prf_in').text()
    profile_info['info']['affiliations']: str = parser.css_first('.gsc_prf_ila').text()
    profile_info['info']['email']: str = parser.css_first('#gsc_prf_ivh').text()
    profile_info['info']['interests']: str = [interest.text() for interest in parser.css('#gsc_prf_int .gs_ibl')]
    
    for co_author in parser.css('.gsc_rsb_aa'):
        profile_info['co-authors'].append({
            'name': co_author.css_first('.gsc_rsb_a_desc a').text(),
            'profile_link': f"https://scholar.google.com{co_author.css_first('.gsc_rsb_a_desc a').attrs['href']}",
            'affiliation': co_author.css_first('.gsc_rsb_a_ext').text(),
        })
    
    page_num: int = 0

    while True:
        driver.get(f'https://scholar.google.com/citations?user={user_id}&hl=en&gl=us&cstart={page_num}&pagesize=100')
        parser = LexborHTMLParser(driver.page_source)
        
        for index, article in enumerate(parser.css('.gsc_a_tr'), start=1):
            try:
                article_title: str = article.css_first('.gsc_a_at').text()
            except: article_title = None
            
            try: 
                article_link: str = f"https://scholar.google.com{article.css_first('.gsc_a_at').attrs['href']}"
            except: article_link = None
            
            try:
                if ',' in article.css_first('.gsc_a_at+ .gs_gray').text():
                    article_authors: List[str] = article.css_first('.gsc_a_at+ .gs_gray').text().split(', ') # list of authors
                else: article_authors: str = article.css_first('.gsc_a_at+ .gs_gray').text()           # single authour
            except: article_authors = None
            
            try:
                article_publication: str = article.css_first('.gs_gray+ .gs_gray').text()
            except: article_publication = None

            try:
                cited_by_count: str = article.css_first('.gsc_a_ac').text() 
            except: cited_by_count = None
            
            try: 
                publication_year: str = article.css_first('.gsc_a_hc').text()
            except: publication_year = None

            profile_info['articles'].append({
                'position': index,
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

    return profile_info
