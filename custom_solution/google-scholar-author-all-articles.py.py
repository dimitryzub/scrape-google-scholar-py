from parsel import Selector
import requests, os, json


def parsel_scrape_all_author_articles():
    params = {
        'user': '_xwYD2sAAAAJ',       # user-id
        'hl': 'en',                   # language
        'gl': 'us',                   # country to search from
        'cstart': 0,                  # articles page. 0 is the first page
        'pagesize': '100'             # articles per page
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    all_articles = []

    while True:
        html = requests.get('https://scholar.google.com/citations', params=params, headers=headers, timeout=30)
        selector = Selector(text=html.text)

        for index, article in enumerate(selector.css('.gsc_a_tr'), start=1):
            article_title = article.css('.gsc_a_at::text').get()
            article_link = f"https://scholar.google.com{article.css('.gsc_a_at::attr(href)').get()}"
            article_authors = article.css('.gsc_a_at+ .gs_gray::text').get()
            article_publication = article.css('.gs_gray+ .gs_gray::text').get()

            cited_by_count = article.css('.gsc_a_ac::text').get()
            publication_year = article.css('.gsc_a_hc::text').get()

            all_articles.append({
                'position': index,
                'title': article_title,
                'link': article_link,
                'authors': article_authors,
                'publication': article_publication,
                'publication_year': publication_year,
                'cited_by_count': cited_by_count
            })

        # this selector is checking for the .class that contains: 'There are no articles in this profile.'
        # example link: https://scholar.google.com/citations?user=VjJm3zYAAAAJ&hl=en&cstart=500&pagesize=100
        if selector.css('.gsc_a_e').get():
            break
        else:
            params['cstart'] += 100  # paginate to the next page

    # [:-1] doesn't pick last element which is not we want and don't contain any data.
    print(json.dumps(all_articles[:-1], indent=2, ensure_ascii=False))
