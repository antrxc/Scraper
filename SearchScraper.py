import requests
from bs4 import BeautifulSoup

# Define the search base URL (replace with your desired search engine)
search_url = "https://www.google.com/search?q={query}"

# Example keyword
query = input("Enter search keyword")
full_url = search_url.format(query=query)

# Fetch the search results page
response = requests.get(full_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract relevant data from search results (adapt selectors as needed)
links = [a['href'] for a in soup.find_all('a', href=True)]
link_list=[]


def has_keyword(link,keyword):
        return keyword in link

for s in links:
        if has_keyword(s,"search"):
                continue
        if has_keyword(s,"url"):
                link_list.append(s[s.index('=')+1:])

filename=query+".txt"
# Open the file in append mode ('a') and write the links
with open(filename, "a") as f:
    for link in link_list:
        f.write(link + "\n")
