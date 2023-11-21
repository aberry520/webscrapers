import requests
from bs4 import BeautifulSoup

search = input("search: ")
url = 'https://www.walmart.com/search?facet=fulfillment_method_in_store&q=' + search
headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }
page = requests.get(url, headers=headers).text

soup = BeautifulSoup(page, 'html.parser')

item = soup.find_all('div', attrs={'data-testid':'list-view'})

print(page)
print