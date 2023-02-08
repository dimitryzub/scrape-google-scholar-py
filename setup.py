from setuptools import setup

README = ''
with open('README.md', 'r') as readme_file:
    README = readme_file.read()

setup(
    name='scrape-google-scholar-py',
    description = 'Extract data from all Google Scholar pages in Python. Sponsored by SerpApi.',
    url='https://github.com/dimitryzub/scrape-google-scholar',
    version='0.2.2',
    license='MIT',
    author='Dmitiry Zub',
    author_email='dimitryzub@gmail.com',
    maintainer='Dmitiry Zub',
    maintainer_email='dimitryzub@gmail.com',
    long_description_content_type='text/markdown',
    long_description=README,
    include_package_data=True,
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Topic :: Internet',
        'Natural Language :: English',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    keywords=[
            'google scholar',
            'serpapi',
            'scraper',
            'python',
            'python google scholar',
            'python google scholar api',
            'web scraping',
            'python web scraping',
            'research',
            'lexbor',
            'selectolax',
            'selenium',
            'selenium-stealth',
            'pandas',
        ],
    install_requires=[
          'google-search-results',
          'selectolax',
          'selenium-stealth',
          'pandas',
    ],
    extras_require={
        'dev':[
            'ruff', #TODO: add test dev dependencies
        ]
    },
    project_urls={
        'Documentation': 'https://github.com/dimitryzub/scrape-google-scholar#example-usage-custom-backend',
        'Source': 'https://github.com/dimitryzub/scrape-google-scholar',
        'Tracker': 'https://github.com/dimitryzub/scrape-google-scholar/issues',
    },
)