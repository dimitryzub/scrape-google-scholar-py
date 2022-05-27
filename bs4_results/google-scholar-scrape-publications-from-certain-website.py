from parsel import Selector
import requests, json, os


def check_websites(website: list or str):
    if isinstance(website, str):
        return website                                           # cabdirect.org
    elif isinstance(website, list):
        return " OR ".join([f'site:{site}' for site in website]) # site:cabdirect.org OR site:cab.com


def scrape_website_publications(query: str, website: list or str):
    
    """
    Add a search query and site or multiple websites.

    Following will work:
    ["cabdirect.org", "lololo.com", "brabus.org"] -> list[str]
    ["cabdirect.org"]                             -> list[str]
    "cabdirect.org"                               -> str
    """
    
    # https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    params = {
        "q": f'{query.lower()} {check_websites(website=website)}',  # search query
        "hl": "en",                                                 # language of the search
        "gl": "us"                                                  # country of the search
    }
    
    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }

    html = requests.get("https://scholar.google.com/scholar", params=params, headers=headers, timeout=30)
    selector = Selector(html.text)
    
    publications = []
    
    # iterate over every element from organic results from the first page and extract the data
    for result in selector.css(".gs_r.gs_scl"):
        title = result.css(".gs_rt").xpath("normalize-space()").get()
        link = result.css(".gs_rt a::attr(href)").get()
        result_id = result.attrib["data-cid"]
        snippet = result.css(".gs_rs::text").get()
        publication_info = result.css(".gs_a").xpath("normalize-space()").get()
        cite_by_link = f'https://scholar.google.com/scholar{result.css(".gs_or_btn.gs_nph+ a::attr(href)").get()}'
        all_versions_link = f'https://scholar.google.com/scholar{result.css("a~ a+ .gs_nph::attr(href)").get()}'
        related_articles_link = f'https://scholar.google.com/scholar{result.css("a:nth-child(4)::attr(href)").get()}'
    
        publications.append({
            "result_id": result_id,
            "title": title,
            "link": link,
            "snippet": snippet,
            "publication_info": publication_info,
            "cite_by_link": cite_by_link,
            "all_versions_link": all_versions_link,
            "related_articles_link": related_articles_link,
        })
    
    # print or return the results
    # return publications

    print(json.dumps(publications, indent=2, ensure_ascii=False))
    

scrape_website_publications(query="biology", website="cabdirect.org")
