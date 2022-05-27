# blog post: https://serpapi.com/blog/scrape-google-scholar-profiles-from-a-certain-university-in-python/#code_explanation

from parsel import Selector
import requests, re, json, os
from serpapi import GoogleSearch
from urllib.parse import urlsplit, parse_qsl


def scrape_all_profiles_from_university(label: str, university_name: str) -> list[dict[str]]:
    # https://docs.python-requests.org/en/master/user/quickstart/#passing-parameters-in-urls
    params = {
        "view_op": "search_authors",                       # author results
        "mauthors": f'label:{label} "{university_name}"',  # search query
        "hl": "en",                                        # language
        "astart": 0,                                       # page number
    }

    # https://docs.python-requests.org/en/master/user/quickstart/#custom-headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
        }

    profile_results = []

    profiles_is_present = True
    while profiles_is_present:

        html = requests.get("https://scholar.google.com/citations", params=params, headers=headers, timeout=30)
        select = Selector(html.text)

        print(f"extracting authors at page #{params['astart']}.")

        for profile in select.css(".gs_ai_chpr"):
            name = profile.css(".gs_ai_name a::text").get()
            link = f'https://scholar.google.com{profile.css(".gs_ai_name a::attr(href)").get()}'
            affiliations = profile.css(".gs_ai_aff").xpath("normalize-space()").get()
            email = profile.css(".gs_ai_eml::text").get()
            cited_by = re.search(r"\d+", profile.xpath('//div[@class="gs_ai_cby"]').get()).group()  # Cited by 17143 -> 17143
            interests = profile.css(".gs_ai_one_int::text").getall()

            profile_results.append({
                "profile_name": name,
                "profile_link": link,
                "profile_affiliations": affiliations,
                "profile_email": email,
                "profile_city_by_count": cited_by,
                "profile_interests": interests,
                })

        # if next page token is present -> update next page token and increment 10 to get the next page
        if select.css("button.gs_btnPR::attr(onclick)").get():
            # https://regex101.com/r/e0mq0C/1
            params["after_author"] = re.search(r"after_author\\x3d(.*)\\x26",
                                               select.css("button.gs_btnPR::attr(onclick)").get()).group(1)  # -> XB0HAMS9__8J
            params["astart"] += 10
        else:
            profiles_is_present = False

    return profile_results


# print(scrape_all_profiles_from_university(label="Deep_Learning", university_name="Harvard University"))
print(json.dumps(scrape_all_profiles_from_university(label="Deep_Learning", university_name="Harvard University"), indent=2))


def serpapi_scrape_all_profiles_from_university(label: str, university_name: str) -> list[dict[str]]:
    params = {
        "api_key": os.getenv("API_KEY"),                    # SerpApi API key
        "engine": "google_scholar_profiles",                # profile results search engine
        "mauthors": f'label:{label} "{university_name}"',   # search query
    }
    search = GoogleSearch(params)

    profile_results_data = []

    profiles_is_present = True
    while profiles_is_present:
        profile_results = search.get_dict()

        for profile in profile_results["profiles"]:

            print(f'Currently extracting {profile["name"]} with {profile["author_id"]} ID.')

            thumbnail = profile["thumbnail"]
            name = profile["name"]
            link = profile["link"]
            author_id = profile["author_id"]
            affiliations = profile["affiliations"]
            email = profile.get("email")
            cited_by = profile.get("cited_by")
            interests = profile.get("interests")

            profile_results_data.append({
                "thumbnail": thumbnail,
                "name": name,
                "link": link,
                "author_id": author_id,
                "email": email,
                "affiliations": affiliations,
                "cited_by": cited_by,
                "interests": interests,
            })

            if "next" in profile_results.get("pagination", []):
                # split URL in parts as a dict and update search "params" variable to a new page that will be passed to GoogleSearch()
                search.params_dict.update(dict(parse_qsl(urlsplit(profile_results.get("pagination").get("next")).query)))
            else:
                profiles_is_present = False

    return profile_results_data

# print(json.dumps(serpapi_scrape_all_profiles_from_university(label="Deep_Learning", university_name="Harvard University"), indent=2))
