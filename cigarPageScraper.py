from bs4 import BeautifulSoup
import requests

page = requests.get("https://www.cigarpage.com/samplers.html")
soup = BeautifulSoup(page.text, 'html.parser')
cigar_names = soup.findAll('span', attrs={'class':'product-name defaultLink'})
# quotes = soup.findAll('span', attrs={'class':'text'})
# authors = soup.findAll('small', attrs={"class":'author'})
# for quote, author in zip(quotes, authors):
#     print(quote.text + "-" + author.text)

for cigar in zip(cigar_names):
    print(cigar)