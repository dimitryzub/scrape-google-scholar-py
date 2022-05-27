from parsel import Selector
import requests, json, os


def check_sources(source: list or str):
    if isinstance(source, str):
        return source                                             # NIPS
    elif isinstance(source, list):
        return " OR ".join([f'source:{item}' for item in source]) # source:NIPS OR source:Neural Information


def scrape_conference_publications(query: str, source: list or str):
    # https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    params = {
        "q": f'{query.lower()} {check_sources(source=source)}',  # search query
        "hl": "en",                         # language of the search
        "gl": "us"                          # country of the search
    }

    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
    }

    html = requests.get("https://scholar.google.com/scholar", params=params, headers=headers, timeout=30)
    selector = Selector(html.text)
    
    publications = []
    
    for result in selector.css(".gs_r.gs_scl"):
        title = result.css(".gs_rt").xpath("normalize-space()").get()
        link = result.css(".gs_rt a::attr(href)").get()
        result_id = result.attrib["data-cid"]
        snippet = result.css(".gs_rs::text").get()
        publication_info = result.css(".gs_a").xpath("normalize-space()").get()
        cite_by_link = f'https://scholar.google.com/scholar{result.css(".gs_or_btn.gs_nph+ a::attr(href)").get()}'
        all_versions_link = f'https://scholar.google.com/scholar{result.css("a~ a+ .gs_nph::attr(href)").get()}'
        related_articles_link = f'https://scholar.google.com/scholar{result.css("a:nth-child(4)::attr(href)").get()}'
        pdf_file_title = result.css(".gs_or_ggsm a").xpath("normalize-space()").get()
        pdf_file_link = result.css(".gs_or_ggsm a::attr(href)").get()
    
        publications.append({
            "result_id": result_id,
            "title": title,
            "link": link,
            "snippet": snippet,
            "publication_info": publication_info,
            "cite_by_link": cite_by_link,
            "all_versions_link": all_versions_link,
            "related_articles_link": related_articles_link,
            "pdf": {
                "title": pdf_file_title,
                "link": pdf_file_link
            }
        })
        
    # return publications

    print(json.dumps(publications, indent=2, ensure_ascii=False))
    

scrape_conference_publications(query="anatomy", source=["NIPS", "Neural Information"])
