## Requirements
Requires Google Chrome and a LinkedIn account.

## Usage example
```python
from scraper.LinkedIn import LinkedIn
from scraper.Search import Search
from scraper.Job import Job


credentials = {
    'email': 'example@mail.com',
    'password': 'DontHackMePlz'
}

linkedin = LinkedIn(requests_per_minute=20)
linkedin.login(credentials)

query = {
    'keywords': 'data analyst',
    'location': 'European union'
}

search = Search(query)
for page_number in search.page_range():
    search.go_to_page(page_number)
    urls = search.get_urls()
    for url in urls:
        job = Job(url).as_dict()
        print(job)

linkedin.close()
```

## Disclaimer
This module is provided for educational purposes only.
Using web scraping software on LinkedIn violates their user agreement.
