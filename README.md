<p align="center">
  <img src="https://user-images.githubusercontent.com/78694043/170675316-0d7be468-3a85-43b7-9151-260e4f2c1c7e.png" />
</p>


This repository is meant to extract data from all Google Scholar pages. You can also use [`scholary`](https://github.com/scholarly-python-package/scholarly) instead. However, it only extracts author and publication data.  

Currently, scripts from this repo extract data from:

1. [Organic results page](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=blizzard&btnG=&oq=blizz) (with pagination).
2. [Profile results page](https://scholar.google.com/citations?view_op=search_authors&mauthors=blizzard&hl=en&oi=drw) (with pagination).
3. [Authour page + author articles](https://scholar.google.com/citations?user=6IQ8pQwAAAAJ&hl=en&oi=sra) (with pagination), everything except "cited by" graph.
4. [Public access mandates metrics page](https://scholar.google.com/citations?view_op=mandates_leaderboard&hl=en). Yes, you can download CSV with one click, however, it doesn't contain a funder link. Script here has it and saves to CSV/JSON.
5. [Top publications metrics page](https://scholar.google.com/citations?view_op=top_venues&hl=en). Categories is also supported (as function argument). Saves to CSV/JSON. Sub-categories are not yet supported.
6. soon: [journal articles page](https://github.com/dimitryzub/scrape-google-scholar/issues/2).

<details>
<summary>Things it doesn't support yet with the new update</summary>

1. Organic results filters (case law, sorting, period ranges). You can add those URL parameters yourself easily to the `google_scholar_organic_search.py` file (line `123`, `136`), where `driver.get()` is being called.
2. Author page -> cited by graph.
3. Extracting [journal articles page](https://scholar.google.com/citations?hl=uk&vq=en&view_op=list_hcore&venue=9oNLl9DgMnQJ.2022). The [issue to add this page is open](https://github.com/dimitryzub/scrape-google-scholar/issues/2).
4. [Top publications metrics page](https://scholar.google.com/citations?view_op=top_venues&hl=en). Subcategories are not yet supported, it's in a TODO list. 
5. Update [cite results](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=blizzard+effects+xanax&oq=blizzard+effects+x#d=gs_cit&t=1674718593252&u=%2Fscholar%3Fq%3Dinfo%3Alm-jhjzd72UJ%3Ascholar.google.com%2F%26output%3Dcite%26scirp%3D7%26hl%3Den) page extraction.

</details>

## Example usage

Say you cloned this repo and use `example_usage.py` file located in the root of the folder:

```python
from custom_solution.google_scholar_profiles_results import scrape_google_scholar_profiles
import json

# Google Scholar search operators could also be used:
# label:computer_vision "Michigan State University"|"U.Michigan"
# this will search all profiles from 2 universities based on computer vision query
data = scrape_google_scholar_profiles(query='blizzard', pagination=False, operating_system='win')

for profile in data:
    print(profile['name'])
    print(profile['interests'])

print(json.dumps(data, indent=2))
```

<details>
<summary>Output</summary>

Regular print: 

```lang-none
Adam Lobel
['Gaming', 'Emotion regulation']
Daniel Blizzard
None
Shuo Chen
['Machine Learning', 'Data Mining', 'Artificial Intelligence']
Ian Livingston
['Human-computer interaction', 'User Experience', 'Player Experience', 'User Research', 'Games']
Minli Xu
['Game', 'Machine Learning', 'Data Science', 'Bioinformatics']
Je Seok Lee
['HCI', 'Player Experience', 'Games', 'Esports']
Alisha Ness
None
Xingyu (Alfred) Liu
['Machine Learning in Game Development']
Amanda LL Cullen
['Games Studies', 'Fan Studies', 'Live Streaming']
Nicole "Nikki" Crenshaw
['MMOs', 'Neoliberalism', 'Social Affordances', 'Identity', 'Accessibility']
```

And a JSON:

```json
[
  {
    "name": "Adam Lobel",
    "link": "https://scholar.google.com/citations?hl=en&user=_xwYD2sAAAAJ",
    "affiliations": "Blizzard Entertainment",
    "interests": [
      "Gaming",
      "Emotion regulation"
    ],
    "email": "Verified email at AdamLobel.com",
    "cited_by_count": 3593
  },
  {
    "name": "Daniel Blizzard",
    "link": "https://scholar.google.com/citations?hl=en&user=dk4LWEgAAAAJ",
    "affiliations": "",
    "interests": null,
    "email": null,
    "cited_by_count": 1041
  },
  {
    "name": "Shuo Chen",
    "link": "https://scholar.google.com/citations?hl=en&user=OBf4YnkAAAAJ",
    "affiliations": "Senior Data Scientist, Blizzard Entertainment",
    "interests": [
      "Machine Learning",
      "Data Mining",
      "Artificial Intelligence"
    ],
    "email": "Verified email at cs.cornell.edu",
    "cited_by_count": 725
  },
  {
    "name": "Ian Livingston",
    "link": "https://scholar.google.com/citations?hl=en&user=xBHVqNIAAAAJ",
    "affiliations": "Blizzard Entertainment",
    "interests": [
      "Human-computer interaction",
      "User Experience",
      "Player Experience",
      "User Research",
      "Games"
    ],
    "email": "Verified email at usask.ca",
    "cited_by_count": 652
  },
  {
    "name": "Minli Xu",
    "link": "https://scholar.google.com/citations?hl=en&user=QST5iogAAAAJ",
    "affiliations": "Blizzard Entertainment",
    "interests": [
      "Game",
      "Machine Learning",
      "Data Science",
      "Bioinformatics"
    ],
    "email": "Verified email at blizzard.com",
    "cited_by_count": 541
  },
  {
    "name": "Je Seok Lee",
    "link": "https://scholar.google.com/citations?hl=en&user=vuvtlzQAAAAJ",
    "affiliations": "Blizzard Entertainment",
    "interests": [
      "HCI",
      "Player Experience",
      "Games",
      "Esports"
    ],
    "email": "Verified email at uci.edu",
    "cited_by_count": 386
  },
  {
    "name": "Alisha Ness",
    "link": "https://scholar.google.com/citations?hl=en&user=xQuwVfkAAAAJ",
    "affiliations": "Activision Blizzard",
    "interests": null,
    "email": null,
    "cited_by_count": 324
  },
  {
    "name": "Xingyu (Alfred) Liu",
    "link": "https://scholar.google.com/citations?hl=en&user=VW9ukOwAAAAJ",
    "affiliations": "Blizzard Entertainment",
    "interests": [
      "Machine Learning in Game Development"
    ],
    "email": null,
    "cited_by_count": 256
  },
  {
    "name": "Amanda LL Cullen",
    "link": "https://scholar.google.com/citations?hl=en&user=oqna6OgAAAAJ",
    "affiliations": "Blizzard Entertainment",
    "interests": [
      "Games Studies",
      "Fan Studies",
      "Live Streaming"
    ],
    "email": null,
    "cited_by_count": 247
  },
  {
    "name": "Nicole \"Nikki\" Crenshaw",
    "link": "https://scholar.google.com/citations?hl=en&user=zmRH6E0AAAAJ",
    "affiliations": "Blizzard Entertainment",
    "interests": [
      "MMOs",
      "Neoliberalism",
      "Social Affordances",
      "Identity",
      "Accessibility"
    ],
    "email": "Verified email at uci.edu",
    "cited_by_count": 202
  }
]
```

</details>


Saving organic results to CSV:

```python
from custom_solution.google_scholar_organic_search import scrape_google_scholar_organic_results

# CSV (JSON also supported) file will be created in the same folder near the runnable script
scrape_google_scholar_organic_results(query='blizzard', pagination=False, operating_system='win', save_to_csv=True)
```

## Prerequisites

This project depends on:
- [`selenium-stealth`](https://github.com/diprajpatra/selenium-stealth) - to bypass CAPTCHAs.
- [`selectolax`](https://github.com/rushter/selectolax) - to parse HTML fast. Its the fastest Python parser wrapped around [`lexbor`](https://github.com/lexbor/lexbor) (parser in pure C)
- [`pandas`](https://pandas.pydata.org/) - to save extracted data to CSV or JSON, or if you want to analyze the data right away. Save options is used in organic results and top publications, public access mandates pages for now.

All scripts are using headless [`selenium-stealth`](https://github.com/diprajpatra/selenium-stealth) to bypass CAPTCHA that appears on Google Scholar, so you need to have a `chromedriver`. If you're on Linux you may need to do additional troubleshooting if `chromedriver` won't run properly. It is not related to the repository itself.

If me or another maintainer of the repository didn't update the driver to a newer version and you want to use a newer one, head over to https://chromedriver.chromium.org/ and download a last stable release either for Linux or Windows, and update `chromedriver` in the `custom_solution/` folder.

## Contributing

Feel free to open an issue. Suggesting what bug you found, something isn't working, what feature to add, or anything else related to Google Scholar.

Tests are not yet added. If you want to add tests, feel free to do so 👍

There's exists a `.gitpod.yaml` config if you're using Gitpod. 

## Licence

`scrape-google-scholar` repository is licensed under MIT license.

<p align="center">Sponsored by <a href="https://serpapi.com/">SerpApi</a> 💛</p>