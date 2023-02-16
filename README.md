<p align="center">
  <img src="https://user-images.githubusercontent.com/78694043/170675316-0d7be468-3a85-43b7-9151-260e4f2c1c7e.png" />
</p>


This repository is meant to extract data from all Google Scholar pages. You have two simple backend options: custom and [SerpApi](http://serpapi.com/).

## 🧐Why two backends?

1. If you don't want to pay for API, custom backend is made for you. However, I'm not 100% sure if `selenium-stealth` could handle all CAPTCHAs (although it handles CAPTCHA by Cloudflare) and similar blocks.
2. If you know about SerpApi but don't want to figure out pagination.
3. SerpApi backend is more reliable because of dedicated pool of proxies, CAPTCHA solvers, parser maintenance, and more.


## 🧩Custom backend supports

You can use [`scholary`](https://github.com/scholarly-python-package/scholarly) to parse the data instead. However, it only extracts first 3 points below.  

1. [Organic results](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=blizzard&btnG=&oq=blizz) (with pagination).
2. [Profile results](https://scholar.google.com/citations?view_op=search_authors&mauthors=blizzard&hl=en&oi=drw) (with pagination).
3. [Author + author articles](https://scholar.google.com/citations?user=6IQ8pQwAAAAJ&hl=en&oi=sra) (with pagination), everything except "cited by" graph.
4. [Public access mandates metrics](https://scholar.google.com/citations?view_op=mandates_leaderboard&hl=en). Yes, you can download CSV with one click, however, it doesn't contain a funder link. Script here has it and saves to CSV/JSON.
5. [Top publications metrics](https://scholar.google.com/citations?view_op=top_venues&hl=en). Categories is also supported (as function argument). Saves to CSV/JSON. Sub-categories are not yet supported.
6. soon: [journal articles](https://github.com/dimitryzub/scrape-google-scholar/issues/2).

<details>
<summary>Things custom backend doesn't support yet</summary>

1. Organic results filters (case law, sorting, period ranges). You can add those URL parameters yourself ([if installing from source](https://github.com/dimitryzub/scrape-google-scholar-py#installing)) easily to the `google_scholar_py/custom_backend/organic_search.py` file (line [`147`](https://github.com/dimitryzub/scrape-google-scholar-py/blob/a6b3b39042eabdc84851e3c1ca3c246e55bf19d1/google_scholar_py/custom_backend/organic_search.py#L147) or [`136`](https://github.com/dimitryzub/scrape-google-scholar-py/blob/a6b3b39042eabdc84851e3c1ca3c246e55bf19d1/google_scholar_py/custom_backend/organic_search.py#L160)), where `driver.get()` is being called.
2. Author page -> cited by graph.
3. Extracting [journal articles page](https://scholar.google.com/citations?hl=uk&vq=en&view_op=list_hcore&venue=9oNLl9DgMnQJ.2022). The [issue to add this page is open](https://github.com/dimitryzub/scrape-google-scholar/issues/2).
4. [Top publications metrics page](https://scholar.google.com/citations?view_op=top_venues&hl=en). Subcategories are not yet supported, it's in a TODO list. 
5. Update [cite results](https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=blizzard+effects+xanax&oq=blizzard+effects+x#d=gs_cit&t=1674718593252&u=%2Fscholar%3Fq%3Dinfo%3Alm-jhjzd72UJ%3Ascholar.google.com%2F%26output%3Dcite%26scirp%3D7%26hl%3Den) page extraction.

</details>

## 🔮SerpApi backend supports

- [Google Scholar Organic](https://serpapi.com/google-scholar-organic-results)
- [Google Scholar Profiles](https://serpapi.com/google-scholar-profilesapi)
- [Google Scholar Author](https://serpapi.com/google-scholar-author-api)
- [Google Scholar Cite](https://serpapi.com/google-scholar-cite-api)

## 📥Installing

Install via `pip`:

```bash
$ pip install scrape-google-scholar-py
```

Install for development from source:

```bash
$ git clone https://github.com/dimitryzub/scrape-google-scholar-py.git
$ cd scrape-google-scholar-py
$ python setup.py install
```


<details>
<summary>If it throws an error with `selenium-stealth`</summary>

  ```bash
  error: The 'selenium' distribution was not found and is required by selenium-stealth
  ```

  Use this command:

  ```bash
  $ pip install selenium-stealth
  ```
</details>

## 📝Example usage custom backend

```python
from google_scholar_py.custom_backend.organic_search import CustomGoogleScholarOrganic
import json

parser = CustomGoogleScholarProfiles()
data = parser.scrape_google_scholar_profiles(
    query='blizzard',
    operating_system='win', # or 'linux'
    pagination=False,
    save_to_csv=False,
    save_to_json=False
    # other params
)
print(json.dumps(data, indent=2))
```

<details>
<summary>Google Scholar search operators could also be used</summary>

```lang-none
label:computer_vision "Michigan State University"|"U.Michigan"
```

This query will search all profiles from 2 universities based on "computer vision" query.
</details>


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


## 📝Example usage SerpApi backend

```python
from google_scholar_py.serpapi_backend.profile_results import SerpApiGoogleScholarProfiles
import json

profile_parser = SerpApiGoogleScholarProfiles()
data = profile_parser.scrape_google_scholar_profile_results(
    query='blizzard',
    api_key='',
    pagination=False,
    # other params
)
print(json.dumps(data, indent=2))
```

<details>
<summary>Output</summary>

```json
[
  {
    "position": 0,
    "title": "Mining learning and crafting scientific experiments: a literature review on the use of minecraft in education and research",
    "result_id": "61OUs-3P374J",
    "link": "https://www.jstor.org/stable/pdf/jeductechsoci.19.2.355.pdf?&seq=1",
    "snippet": "\u2026 Minecraft have aroused the attention of teachers and researchers alike. To gain insights into the applicability of Minecraft, \u2026 our own considerable experience with Minecraft in courses on \u2026",
    "publication_info": {
      "summary": "S Nebel, S Schneider, GD Rey - Journal of Educational Technology & \u2026, 2016 - JSTOR",
      "authors": [
        {
          "name": "S Nebel",
          "link": "https://scholar.google.com/citations?user=_WTrwUwAAAAJ&hl=en&oi=sra",
          "serpapi_scholar_link": "https://serpapi.com/search.json?author_id=_WTrwUwAAAAJ&engine=google_scholar_author&hl=en", 
          "author_id": "_WTrwUwAAAAJ"
        },
        {
          "name": "S Schneider",
          "link": "https://scholar.google.com/citations?user=6Lh4FBMAAAAJ&hl=en&oi=sra",
          "serpapi_scholar_link": "https://serpapi.com/search.json?author_id=6Lh4FBMAAAAJ&engine=google_scholar_author&hl=en", 
          "author_id": "6Lh4FBMAAAAJ"
        },
        {
          "name": "GD Rey",
          "link": "https://scholar.google.com/citations?user=jCilMQoAAAAJ&hl=en&oi=sra",
          "serpapi_scholar_link": "https://serpapi.com/search.json?author_id=jCilMQoAAAAJ&engine=google_scholar_author&hl=en", 
          "author_id": "jCilMQoAAAAJ"
        }
      ]
    },
    "resources": [
      {
        "title": "researchgate.net",
        "file_format": "PDF",
        "link": "https://www.researchgate.net/profile/Steve-Nebel/publication/301232882_Mining_Learning_and_Crafting_Scientific_Experiments_A_Literature_Review_on_the_Use_of_Minecraft_in_Education_and_Research/links/570e709008aed4bec6fddad4/Mining-Learning-and-Crafting-Scientific-Experiments-A-Literature-Review-on-the-Use-of-Minecraft-in-Education-and-Research.pdf"
      }
    ],
    "inline_links": {
      "serpapi_cite_link": "https://serpapi.com/search.json?engine=google_scholar_cite&q=61OUs-3P374J",
      "cited_by": {
        "total": 358,
        "link": "https://scholar.google.com/scholar?cites=13753940406839825387&as_sdt=2005&sciodt=0,5&hl=en",
        "cites_id": "13753940406839825387",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=2005&cites=13753940406839825387&engine=google_scholar&hl=en"
      },
      "related_pages_link": "https://scholar.google.com/scholar?q=related:61OUs-3P374J:scholar.google.com/&scioq=minecraft&hl=en&as_sdt=0,5",
      "serpapi_related_pages_link": "https://serpapi.com/search.json?as_sdt=0%2C5&engine=google_scholar&hl=en&q=related%3A61OUs-3P374J%3Ascholar.google.com%2F",
      "versions": {
        "total": 10,
        "link": "https://scholar.google.com/scholar?cluster=13753940406839825387&hl=en&as_sdt=0,5",
        "cluster_id": "13753940406839825387",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=0%2C5&cluster=13753940406839825387&engine=google_scholar&hl=en"
      }
    }
  },
  {
    "position": 1,
    "title": "Minecraft, beyond construction and survival",
    "result_id": "_Lo9erywZPUJ",
    "type": "Pdf",
    "link": "https://stacks.stanford.edu/file/druid:qq694ht6771/WellPlayed-v1n1-11.pdf#page=9",
    "snippet": "\" We\u2019ll keep releasing expansions and keep the game alive, but there needs to be some kind of final version that you can point at and say,\u2018I did this!\u2019... I\u2019m not sure why I feel a need to \u2026",
    "publication_info": {
      "summary": "SC Duncan - 2011 - stacks.stanford.edu",
      "authors": [
        {
          "name": "SC Duncan",
          "link": "https://scholar.google.com/citations?user=Ypqv_IEAAAAJ&hl=en&oi=sra",
          "serpapi_scholar_link": "https://serpapi.com/search.json?author_id=Ypqv_IEAAAAJ&engine=google_scholar_author&hl=en", 
          "author_id": "Ypqv_IEAAAAJ"
        }
      ]
    },
    "resources": [
      {
        "title": "stanford.edu",
        "file_format": "PDF",
        "link": "https://stacks.stanford.edu/file/druid:qq694ht6771/WellPlayed-v1n1-11.pdf#page=9"
      }
    ],
    "inline_links": {
      "serpapi_cite_link": "https://serpapi.com/search.json?engine=google_scholar_cite&q=_Lo9erywZPUJ",
      "cited_by": {
        "total": 288,
        "link": "https://scholar.google.com/scholar?cites=17682452360514616060&as_sdt=2005&sciodt=0,5&hl=en",
        "cites_id": "17682452360514616060",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=2005&cites=17682452360514616060&engine=google_scholar&hl=en"
      },
      "related_pages_link": "https://scholar.google.com/scholar?q=related:_Lo9erywZPUJ:scholar.google.com/&scioq=minecraft&hl=en&as_sdt=0,5",
      "serpapi_related_pages_link": "https://serpapi.com/search.json?as_sdt=0%2C5&engine=google_scholar&hl=en&q=related%3A_Lo9erywZPUJ%3Ascholar.google.com%2F",
      "versions": {
        "total": 6,
        "link": "https://scholar.google.com/scholar?cluster=17682452360514616060&hl=en&as_sdt=0,5",
        "cluster_id": "17682452360514616060",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=0%2C5&cluster=17682452360514616060&engine=google_scholar&hl=en"
      },
      "cached_page_link": "https://scholar.googleusercontent.com/scholar?q=cache:_Lo9erywZPUJ:scholar.google.com/+minecraft&hl=en&as_sdt=0,5"
    }
  },
  {
    "position": 2,
    "title": "Minecraft as a creative tool: A case study",
    "result_id": "wOTRJ8q0KIsJ",
    "link": "https://www.igi-global.com/article/minecraft-as-a-creative-tool/116516",
    "snippet": "\u2026 environment, Minecraft. In the following case study, the authors explored the use of Minecraft in \u2026 The authors demonstrate that Minecraft offers a unique opportunity for students to display \u2026",
    "publication_info": {
      "summary": "M Cipollone, CC Schifter, RA Moffat - International Journal of Game \u2026, 2014 - igi-global.com"
    },
    "resources": [
      {
        "title": "minecraft.school.nz",
        "file_format": "PDF",
        "link": "https://www.minecraft.school.nz/uploads/2/9/6/3/2963069/minecraft-as-a-creative-tool_-a-case-study_cipollone2014.pdf"
      }
    ],
    "inline_links": {
      "serpapi_cite_link": "https://serpapi.com/search.json?engine=google_scholar_cite&q=wOTRJ8q0KIsJ",
      "cited_by": {
        "total": 102,
        "link": "https://scholar.google.com/scholar?cites=10027463350684869824&as_sdt=2005&sciodt=0,5&hl=en",
        "cites_id": "10027463350684869824",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=2005&cites=10027463350684869824&engine=google_scholar&hl=en"
      },
      "related_pages_link": "https://scholar.google.com/scholar?q=related:wOTRJ8q0KIsJ:scholar.google.com/&scioq=minecraft&hl=en&as_sdt=0,5",
      "serpapi_related_pages_link": "https://serpapi.com/search.json?as_sdt=0%2C5&engine=google_scholar&hl=en&q=related%3AwOTRJ8q0KIsJ%3Ascholar.google.com%2F",
      "versions": {
        "total": 9,
        "link": "https://scholar.google.com/scholar?cluster=10027463350684869824&hl=en&as_sdt=0,5",
        "cluster_id": "10027463350684869824",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=0%2C5&cluster=10027463350684869824&engine=google_scholar&hl=en"
      }
    }
  },
  {
    "position": 3,
    "title": "Learning mathematics through Minecraft",
    "result_id": "Hh4p5NaYNu0J",
    "link": "https://pubs.nctm.org/abstract/journals/tcm/21/1/article-p56.xml",
    "snippet": "\u2026 Minecraft to explore area and perimeter. First, the teacher reviewed the definition of perimeter and area. Using a class set of iPods with Minecraft \u2026 Minecraft forms a medium to explore \u2026",
    "publication_info": {
      "summary": "B Bos, L Wilder, M Cook, R O'Donnell - Teaching Children \u2026, 2014 - pubs.nctm.org",
      "authors": [
        {
          "name": "B Bos",
          "link": "https://scholar.google.com/citations?user=DfdRg-8AAAAJ&hl=en&oi=sra",
          "serpapi_scholar_link": "https://serpapi.com/search.json?author_id=DfdRg-8AAAAJ&engine=google_scholar_author&hl=en", 
          "author_id": "DfdRg-8AAAAJ"
        }
      ]
    },
    "resources": [
      {
        "title": "researchgate.net",
        "file_format": "PDF",
        "link": "https://www.researchgate.net/profile/Beth-Bos/publication/267507986_Learning_mathematics_through_Minecraft_Authors/links/545103b80cf249aa53dc8eb2/Learning-mathematics-through-Minecraft-Authors.pdf"
      }
    ],
    "inline_links": {
      "serpapi_cite_link": "https://serpapi.com/search.json?engine=google_scholar_cite&q=Hh4p5NaYNu0J",
      "cited_by": {
        "total": 120,
        "link": "https://scholar.google.com/scholar?cites=17093017484449619486&as_sdt=2005&sciodt=0,5&hl=en",
        "cites_id": "17093017484449619486",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=2005&cites=17093017484449619486&engine=google_scholar&hl=en"
      },
      "related_pages_link": "https://scholar.google.com/scholar?q=related:Hh4p5NaYNu0J:scholar.google.com/&scioq=minecraft&hl=en&as_sdt=0,5",
      "serpapi_related_pages_link": "https://serpapi.com/search.json?as_sdt=0%2C5&engine=google_scholar&hl=en&q=related%3AHh4p5NaYNu0J%3Ascholar.google.com%2F",
      "versions": {
        "total": 8,
        "link": "https://scholar.google.com/scholar?cluster=17093017484449619486&hl=en&as_sdt=0,5",
        "cluster_id": "17093017484449619486",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=0%2C5&cluster=17093017484449619486&engine=google_scholar&hl=en"
      }
    }
  },
  {
    "position": 4,
    "title": "A deep hierarchical approach to lifelong learning in minecraft",
    "result_id": "a_Er9i3hDtUJ",
    "link": "https://ojs.aaai.org/index.php/AAAI/article/view/10744",
    "snippet": "We propose a lifelong learning system that has the ability to reuse and transfer knowledge from one task to another while efficiently retaining the previously learned knowledge-base. \u2026",
    "publication_info": {
      "summary": "C Tessler, S Givony, T Zahavy, D Mankowitz\u2026 - Proceedings of the \u2026, 2017 - ojs.aaai.org",
      "authors": [
        {
          "name": "C Tessler",
          "link": "https://scholar.google.com/citations?user=7eLKa3IAAAAJ&hl=en&oi=sra",
          "serpapi_scholar_link": "https://serpapi.com/search.json?author_id=7eLKa3IAAAAJ&engine=google_scholar_author&hl=en", 
          "author_id": "7eLKa3IAAAAJ"
        },
        {
          "name": "S Givony",
          "link": "https://scholar.google.com/citations?user=nlVsO4YAAAAJ&hl=en&oi=sra",
          "serpapi_scholar_link": "https://serpapi.com/search.json?author_id=nlVsO4YAAAAJ&engine=google_scholar_author&hl=en", 
          "author_id": "nlVsO4YAAAAJ"
        },
        {
          "name": "T Zahavy",
          "link": "https://scholar.google.com/citations?user=9dXN6cMAAAAJ&hl=en&oi=sra",
          "serpapi_scholar_link": "https://serpapi.com/search.json?author_id=9dXN6cMAAAAJ&engine=google_scholar_author&hl=en", 
          "author_id": "9dXN6cMAAAAJ"
        },
        {
          "name": "D Mankowitz",
          "link": "https://scholar.google.com/citations?user=v84tWxsAAAAJ&hl=en&oi=sra",
          "serpapi_scholar_link": "https://serpapi.com/search.json?author_id=v84tWxsAAAAJ&engine=google_scholar_author&hl=en", 
          "author_id": "v84tWxsAAAAJ"
        }
      ]
    },
    "resources": [
      {
        "title": "aaai.org",
        "file_format": "PDF",
        "link": "https://ojs.aaai.org/index.php/AAAI/article/view/10744/10603"
      }
    ],
    "inline_links": {
      "serpapi_cite_link": "https://serpapi.com/search.json?engine=google_scholar_cite&q=a_Er9i3hDtUJ",
      "cited_by": {
        "total": 364,
        "link": "https://scholar.google.com/scholar?cites=15352455767272452459&as_sdt=2005&sciodt=0,5&hl=en",
        "cites_id": "15352455767272452459",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=2005&cites=15352455767272452459&engine=google_scholar&hl=en"
      },
      "related_pages_link": "https://scholar.google.com/scholar?q=related:a_Er9i3hDtUJ:scholar.google.com/&scioq=minecraft&hl=en&as_sdt=0,5",
      "serpapi_related_pages_link": "https://serpapi.com/search.json?as_sdt=0%2C5&engine=google_scholar&hl=en&q=related%3Aa_Er9i3hDtUJ%3Ascholar.google.com%2F",
      "versions": {
        "total": 13,
        "link": "https://scholar.google.com/scholar?cluster=15352455767272452459&hl=en&as_sdt=0,5",
        "cluster_id": "15352455767272452459",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=0%2C5&cluster=15352455767272452459&engine=google_scholar&hl=en"
      },
      "cached_page_link": "https://scholar.googleusercontent.com/scholar?q=cache:a_Er9i3hDtUJ:scholar.google.com/+minecraft&hl=en&as_sdt=0,5"
    }
  },
  {
    "position": 5,
    "title": "Teaching scientific concepts using a virtual world: Minecraft.",
    "result_id": "Oh88DuoTaLYJ",
    "link": "https://search.informit.org/doi/abs/10.3316/aeipt.195598",
    "snippet": "Minecraft is a multiplayer sandbox video game based in a virtual world modelled on the real \u2026 of Minecraft lends itself to the teaching of various academic subjects. Minecraft also has a \u2026",
    "publication_info": {
      "summary": "D Short - Teaching science, 2012 - search.informit.org",
      "authors": [
        {
          "name": "D Short",
          "link": "https://scholar.google.com/citations?user=ec_1ZmMAAAAJ&hl=en&oi=sra",
          "serpapi_scholar_link": "https://serpapi.com/search.json?author_id=ec_1ZmMAAAAJ&engine=google_scholar_author&hl=en", 
          "author_id": "ec_1ZmMAAAAJ"
        }
      ]
    },
    "resources": [
      {
        "title": "academia.edu",
        "file_format": "PDF",
        "link": "https://www.academia.edu/download/31153502/Short-2012-MC-Color-Version.pdf"
      }
    ],
    "inline_links": {
      "serpapi_cite_link": "https://serpapi.com/search.json?engine=google_scholar_cite&q=Oh88DuoTaLYJ",
      "cited_by": {
        "total": 274,
        "link": "https://scholar.google.com/scholar?cites=13143777408462888762&as_sdt=2005&sciodt=0,5&hl=en",
        "cites_id": "13143777408462888762",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=2005&cites=13143777408462888762&engine=google_scholar&hl=en"
      },
      "related_pages_link": "https://scholar.google.com/scholar?q=related:Oh88DuoTaLYJ:scholar.google.com/&scioq=minecraft&hl=en&as_sdt=0,5",
      "serpapi_related_pages_link": "https://serpapi.com/search.json?as_sdt=0%2C5&engine=google_scholar&hl=en&q=related%3AOh88DuoTaLYJ%3Ascholar.google.com%2F",
      "versions": {
        "total": 8,
        "link": "https://scholar.google.com/scholar?cluster=13143777408462888762&hl=en&as_sdt=0,5",
        "cluster_id": "13143777408462888762",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=0%2C5&cluster=13143777408462888762&engine=google_scholar&hl=en"
      }
    }
  },
  {
    "position": 6,
    "title": "Investigating the role of Minecraft in educational learning environments",
    "result_id": "6RcOZdlG3CcJ",
    "link": "https://www.tandfonline.com/doi/abs/10.1080/09523987.2016.1254877",
    "snippet": "\u2026 This research paper identifies the way in which Minecraft Edu can be used to contribute to the teaching 
and learning of secondary students via a multiple case research study. Minecraft \u2026",
    "publication_info": {
      "summary": "N Callaghan - Educational Media International, 2016 - Taylor & Francis"
    },
    "inline_links": {
      "serpapi_cite_link": "https://serpapi.com/search.json?engine=google_scholar_cite&q=6RcOZdlG3CcJ",
      "cited_by": {
        "total": 95,
        "link": "https://scholar.google.com/scholar?cites=2872248561872803817&as_sdt=2005&sciodt=0,5&hl=en",
        "cites_id": "2872248561872803817",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=2005&cites=2872248561872803817&engine=google_scholar&hl=en"
      },
      "related_pages_link": "https://scholar.google.com/scholar?q=related:6RcOZdlG3CcJ:scholar.google.com/&scioq=minecraft&hl=en&as_sdt=0,5",
      "serpapi_related_pages_link": "https://serpapi.com/search.json?as_sdt=0%2C5&engine=google_scholar&hl=en&q=related%3A6RcOZdlG3CcJ%3Ascholar.google.com%2F",
      "versions": {
        "total": 3,
        "link": "https://scholar.google.com/scholar?cluster=2872248561872803817&hl=en&as_sdt=0,5",
        "cluster_id": "2872248561872803817",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=0%2C5&cluster=2872248561872803817&engine=google_scholar&hl=en"
      }
    }
  },
  {
    "position": 7,
    "title": "Maker culture and Minecraft: implications for the future of learning",
    "result_id": "h27IfZ5va2YJ",
    "link": "https://www.tandfonline.com/doi/abs/10.1080/09523987.2015.1075103",
    "snippet": "\u2026 be best to subscribe to for gathering information on Minecraft maker culture. From there, we \u2026 the 
Minecraft videos that we are studying \u201ccreators\u201d due to the culture of the Minecraft video \u2026",
    "publication_info": {
      "summary": "DJ Niemeyer, HR Gerber - Educational Media International, 2015 - Taylor & Francis",
      "authors": [
        {
          "name": "DJ Niemeyer",
          "link": "https://scholar.google.com/citations?user=iEZOnzQAAAAJ&hl=en&oi=sra",
          "serpapi_scholar_link": "https://serpapi.com/search.json?author_id=iEZOnzQAAAAJ&engine=google_scholar_author&hl=en", 
          "author_id": "iEZOnzQAAAAJ"
        },
        {
          "name": "HR Gerber",
          "link": "https://scholar.google.com/citations?user=DwyCTMUAAAAJ&hl=en&oi=sra",
          "serpapi_scholar_link": "https://serpapi.com/search.json?author_id=DwyCTMUAAAAJ&engine=google_scholar_author&hl=en", 
          "author_id": "DwyCTMUAAAAJ"
        }
      ]
    },
    "resources": [
      {
        "title": "publicservicesalliance.org",
        "file_format": "PDF",
        "link": "http://publicservicesalliance.org/wp-content/uploads/2016/06/Maker_culture_and_Minecraft_implications.pdf"    
      }
    ],
    "inline_links": {
      "serpapi_cite_link": "https://serpapi.com/search.json?engine=google_scholar_cite&q=h27IfZ5va2YJ",
      "cited_by": {
        "total": 114,
        "link": "https://scholar.google.com/scholar?cites=7380115140882493063&as_sdt=2005&sciodt=0,5&hl=en",
        "cites_id": "7380115140882493063",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=2005&cites=7380115140882493063&engine=google_scholar&hl=en"
      },
      "related_pages_link": "https://scholar.google.com/scholar?q=related:h27IfZ5va2YJ:scholar.google.com/&scioq=minecraft&hl=en&as_sdt=0,5",
      "serpapi_related_pages_link": "https://serpapi.com/search.json?as_sdt=0%2C5&engine=google_scholar&hl=en&q=related%3Ah27IfZ5va2YJ%3Ascholar.google.com%2F",
      "versions": {
        "total": 8,
        "link": "https://scholar.google.com/scholar?cluster=7380115140882493063&hl=en&as_sdt=0,5",
        "cluster_id": "7380115140882493063",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=0%2C5&cluster=7380115140882493063&engine=google_scholar&hl=en"
      }
    }
  },
  {
    "position": 8,
    "title": "Control of memory, active perception, and action in minecraft",
    "result_id": "-5uM8qRUviwJ",
    "link": "http://proceedings.mlr.press/v48/oh16.html",
    "snippet": "In this paper, we introduce a new set of reinforcement learning (RL) tasks in Minecraft (a flexible 3D world). 
We then use these tasks to systematically compare and contrast existing \u2026",
    "publication_info": {
      "summary": "J Oh, V Chockalingam, H Lee - \u2026 conference on machine \u2026, 2016 - proceedings.mlr.press",
      "authors": [
        {
          "name": "J Oh",
          "link": "https://scholar.google.com/citations?user=LNUeOu4AAAAJ&hl=en&oi=sra",
          "serpapi_scholar_link": "https://serpapi.com/search.json?author_id=LNUeOu4AAAAJ&engine=google_scholar_author&hl=en", 
          "author_id": "LNUeOu4AAAAJ"
        },
        {
          "name": "V Chockalingam",
          "link": "https://scholar.google.com/citations?user=CM2UkioAAAAJ&hl=en&oi=sra",
          "serpapi_scholar_link": "https://serpapi.com/search.json?author_id=CM2UkioAAAAJ&engine=google_scholar_author&hl=en", 
          "author_id": "CM2UkioAAAAJ"
        },
        {
          "name": "H Lee",
          "link": "https://scholar.google.com/citations?user=fmSHtE8AAAAJ&hl=en&oi=sra",
          "serpapi_scholar_link": "https://serpapi.com/search.json?author_id=fmSHtE8AAAAJ&engine=google_scholar_author&hl=en", 
          "author_id": "fmSHtE8AAAAJ"
        }
      ]
    },
    "resources": [
      {
        "title": "mlr.press",
        "file_format": "PDF",
        "link": "http://proceedings.mlr.press/v48/oh16.pdf"
      }
    ],
    "inline_links": {
      "serpapi_cite_link": "https://serpapi.com/search.json?engine=google_scholar_cite&q=-5uM8qRUviwJ",
      "cited_by": {
        "total": 317,
        "link": "https://scholar.google.com/scholar?cites=3224107450664524795&as_sdt=2005&sciodt=0,5&hl=en",
        "cites_id": "3224107450664524795",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=2005&cites=3224107450664524795&engine=google_scholar&hl=en"
      },
      "related_pages_link": "https://scholar.google.com/scholar?q=related:-5uM8qRUviwJ:scholar.google.com/&scioq=minecraft&hl=en&as_sdt=0,5",
      "serpapi_related_pages_link": "https://serpapi.com/search.json?as_sdt=0%2C5&engine=google_scholar&hl=en&q=related%3A-5uM8qRUviwJ%3Ascholar.google.com%2F",
      "versions": {
        "total": 7,
        "link": "https://scholar.google.com/scholar?cluster=3224107450664524795&hl=en&as_sdt=0,5",
        "cluster_id": "3224107450664524795",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=0%2C5&cluster=3224107450664524795&engine=google_scholar&hl=en"
      },
      "cached_page_link": "http://scholar.googleusercontent.com/scholar?q=cache:-5uM8qRUviwJ:scholar.google.com/+minecraft&hl=en&as_sdt=0,5"
    }
  },
  {
    "position": 9,
    "title": "Minecraft as a teaching tool: One case study",
    "result_id": "yItxbN8DVXYJ",
    "link": "https://www.learntechlib.org/p/48540/",
    "snippet": "We know games help students gain skills and insights in many ways, and that games are engaging. With new online MMOPRPG games, like Minecraft, what we do not know is what \u2026",
    "publication_info": {
      "summary": "C Schifter, M Cipollone - Society for Information Technology & \u2026, 2013 - learntechlib.org"
    },
    "inline_links": {
      "serpapi_cite_link": "https://serpapi.com/search.json?engine=google_scholar_cite&q=yItxbN8DVXYJ",
      "cited_by": {
        "total": 55,
        "link": "https://scholar.google.com/scholar?cites=8526725727627873224&as_sdt=2005&sciodt=0,5&hl=en",
        "cites_id": "8526725727627873224",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=2005&cites=8526725727627873224&engine=google_scholar&hl=en"
      },
      "related_pages_link": "https://scholar.google.com/scholar?q=related:yItxbN8DVXYJ:scholar.google.com/&scioq=minecraft&hl=en&as_sdt=0,5",
      "serpapi_related_pages_link": "https://serpapi.com/search.json?as_sdt=0%2C5&engine=google_scholar&hl=en&q=related%3AyItxbN8DVXYJ%3Ascholar.google.com%2F",
      "versions": {
        "total": 2,
        "link": "https://scholar.google.com/scholar?cluster=8526725727627873224&hl=en&as_sdt=0,5",
        "cluster_id": "8526725727627873224",
        "serpapi_scholar_link": "https://serpapi.com/search.json?as_sdt=0%2C5&cluster=8526725727627873224&engine=google_scholar&hl=en"
      }
    }
  }
]
```

</details>

## 🕹Dependencies

This project depends on:
- [`selenium-stealth`](https://github.com/diprajpatra/selenium-stealth) - to bypass CAPTCHAs.
- [`selectolax`](https://github.com/rushter/selectolax) - to parse HTML fast. Its the fastest Python parser wrapped around [`lexbor`](https://github.com/lexbor/lexbor) (parser in pure C).
- [`pandas`](https://pandas.pydata.org/) - to save extracted data to CSV or JSON, or if you want to analyze the data right away. Save options is used in organic results and top publications, public access mandates pages for now.
- [`google-search-results`](https://github.com/serpapi/google-search-results-python) - Python wrapper for SerpApi backend.
- [other packages in the `requirements.txt`](https://github.com/dimitryzub/scrape-google-scholar-py/blob/8de484e0eec71478e330303fb405a22e0178f068/requirements.txt).

All scripts are using headless [`selenium-stealth`](https://github.com/diprajpatra/selenium-stealth) to bypass CAPTCHA that appears on Google Scholar, so you need to have a `chromedriver`. If you're on Linux you may need to do additional troubleshooting if `chromedriver` won't run properly.

If me or another maintainer of the repository didn't update the driver to a newer version and you want to use a newer one, head over to https://chromedriver.chromium.org/ and download a last stable release either for Linux or Windows, and update `chromedriver` in the `custom_solution/` folder.

## ✍Contributing

Feel free to open an issue suggesting what bug you found, something isn't working, what feature to add, or anything else related to Google Scholar.

If you find comfortable to open a PR, feel free to do so. Guidelines are simple: conventional commits + code as simple as possible without unnecessary complexity.

There's exists a `.gitpod.yaml` config if you're using [Gitpod](https://www.gitpod.io/). 

## 📜Licence

`scrape-google-scholar` repository is licensed under MIT license.

<p align="center">Sponsored by <a href="https://serpapi.com/">SerpApi</a> 💛</p>