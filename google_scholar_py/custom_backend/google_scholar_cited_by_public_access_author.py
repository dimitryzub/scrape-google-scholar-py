from parsel import Selector
import requests, json

#TODO: add cited by graph extraction to author script

def parsel_scrape_author_cited_by_graph():
    params = {
        'user': '_xwYD2sAAAAJ',       # user-id
        'hl': 'en'                    # language
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    data = {
        'cited_by': [],
        'graph': []
    }

    html = requests.get('https://scholar.google.com/citations', params=params, headers=headers, timeout=30)
    selector = Selector(text=html.text)

    since_year = selector.css('.gsc_rsb_sth~ .gsc_rsb_sth+ .gsc_rsb_sth::text').get().lower().replace(' ', '_')

    for cited_by_public_access in selector.css('.gsc_rsb'):
        data['cited_by'].append({
            'citations_all': cited_by_public_access.css('tr:nth-child(1) .gsc_rsb_sc1+ .gsc_rsb_std::text').get(),
            f'citations_since_{since_year}': cited_by_public_access.css('tr:nth-child(1) .gsc_rsb_std+ .gsc_rsb_std::text').get(),
            'h_index_all': cited_by_public_access.css('tr:nth-child(2) .gsc_rsb_sc1+ .gsc_rsb_std::text').get(),
            f'h_index_since_{since_year}': cited_by_public_access.css('tr:nth-child(2) .gsc_rsb_std+ .gsc_rsb_std::text').get(),
            'i10_index_all': cited_by_public_access.css('tr~ tr+ tr .gsc_rsb_sc1+ .gsc_rsb_std::text').get(),
            f'i10_index_since_{since_year}': cited_by_public_access.css('tr~ tr+ tr .gsc_rsb_std+ .gsc_rsb_std::text').get(),
            'articles': {
                    'available': int(cited_by_public_access.css('.gsc_rsb_m_a:nth-child(1) span::text').get().split(' ')[0]), # to get only digit value
                    'not_available': int(cited_by_public_access.css('.gsc_rsb_m_na div::text').get().split(' ')[0]),          # to get only digit value
                },
            'articles_link': f"https://scholar.google.com{cited_by_public_access.css('#gsc_lwp_mndt_lnk::attr(href)').get()}"
        })
    
    for graph_year, graph_yaer_value in zip(selector.css('.gsc_g_t::text'), selector.css('.gsc_g_al::text')):
        data['graph'].append({
            'year': graph_year.get(),
            'value': int(graph_yaer_value.get())
        })

if __name__ == '__main__':
    print(json.dumps(parsel_scrape_author_cited_by_graph(), indent=2, ensure_ascii=False))
