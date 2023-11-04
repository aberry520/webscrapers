import requests
from bs4 import BeautifulSoup

search = input("search: ")
url = 'https://www.google.com/search?tbm=isch&q=site:cigarpage.com+' + search

page = requests.get(url).text

soup = BeautifulSoup(page, 'html.parser')

# Create a variable to store the second image.
second_image = None

# Iterate over the results and check if the link is valid.
counter = 0
for raw_img in soup.find_all('img'):
  link = raw_img.get('src')
  if link:
    counter += 1

    # If the counter is equal to 2, store the link in the variable.
    if counter == 2:
      second_image = link

      # Break out of the loop.
      break

# Print the second image.
if second_image:
  print(second_image)
else:
  print("No results found.")

# import requests
# from bs4 import BeautifulSoup
# search = input("search: ")
# url = 'https://www.google.com/search?tbm=isch&q=site:cigarpage.com+' + search

# # page = open('tower.html', 'r').read()
# page = requests.get(url).text

# soup = BeautifulSoup(page, 'html.parser')

# for raw_img in soup.find_all('img'):
#   link = raw_img.get('src')
#   if link:
#     print(link)