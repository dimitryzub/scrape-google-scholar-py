from serpapi import GoogleSearch
import os

def organic_results():
    params = {
        "api_key": os.getenv("API_KEY"),      # serpapi api key
        "engine": "google_scholar",           # serpapi parsing engine
        "q": "blizzard",                      # search query
        "hl": "en"                            # language
    }

    search = GoogleScholarSearch(params)
    results = search.get_dict()

    return [result["result_id"] for result in results["organic_results"]]


def cite_results():

    citations = []

    for citation_id in organic_results():
        params = {
            "api_key": os.getenv("API_KEY"),
            "engine": "google_scholar_cite",
            "q": citation_id
        }

        search = GoogleScholarSearch(params)
        results = search.get_dict()

        for result in results["citations"]:
            institution = result["title"]
            citation = result["snippet"]

            citations.append({
                "institution": institution,
                "citations": citation
            })

    return citations
