from parsel import Selector
import requests, os, json, re


def parsel_scrape_author_co_authors():
    params = {
        'user': '_xwYD2sAAAAJ',       # user-id
        'hl': 'en'                    # language
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }

    co_authors = []

    html = requests.get('https://scholar.google.com/citations', params=params, headers=headers, timeout=30)
    selector = Selector(text=html.text)

    for result in selector.css('.gsc_rsb_aa'):
        co_authors.append({
            'name': result.css('.gsc_rsb_a_desc a::text').get(),
            'title': result.css('.gsc_rsb_a_ext::text').get(),
            'link': f"https://scholar.google.com{result.css('.gsc_rsb_a_desc a::attr(href)').get()}",
            'email': result.css('.gsc_rsb_a_ext.gsc_rsb_a_ext2::text').get(),
            # https://regex101.com/r/awJNhL/1
            'thumbnail': f"https://scholar.googleusercontent.com/citations?view_op=view_photo&user={re.search(r'user=(.*)&', result.css('.gsc_rsb_a_desc a::attr(href)').get()).group(1)}"
        })

    print(json.dumps(co_authors, indent=2, ensure_ascii=False))
