import cloudscraper

payload = {
    "operationName": "GetCategories",
    "variables": {
        "currentPage": 1,
        "id": "Nw==",
        "filters": {
            "available_to_book": {"in": ["179", "336"]},
            "city": {"in": ["25"]},
            "category_uid": {"eq": "Nw=="},
        },
        "pageSize": 30,
        "sort": {"available_startdate": "ASC"},
    },
    "query": "query GetCategories($id: String!, $pageSize: Int!, $currentPage: Int!, $filters: ProductAttributeFilterInput!, $sort: ProductAttributeSortInput) { categories(filters: {category_uid: {in: [$id]}}) { items { uid meta_title __typename } __typename } products(pageSize: $pageSize, currentPage: $currentPage, filter: $filters, sort: $sort) { items { name city available_startdate } total_count __typename } }",
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
}
scraper = cloudscraper.create_scraper(
    browser="chrome"
)  # Returns a requests.Session object
response = scraper.post(
    "https://api.holland2stay.com/graphql/", json=payload, headers=headers
)

print(response.content)
