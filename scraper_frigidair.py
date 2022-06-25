import requests, re, json
from bs4 import BeautifulSoup

session = requests.Session()

URL = "https://www.frigidaire.ca/Kitchen/Refrigerators/View-All/"

my_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "if-modified-since": "Sun, 05 Jun 2022 18:50:28 GMT",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36"
  }

page = session.get(URL, headers=my_headers)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find_all("script", {"type": "text/javascript"}) # The data that I believe we want is stored in a script

script_with_data = results[4].get_text() # This relies on the location being the 4th item in the list. May need to find a better way of locating this script so that it doesn't brake if the website structure is changed

# Take the script that is just text, and find the bit that we need
data_index_start = script_with_data.find("var FilterItems = ") + len("var FilterItems = ")
data_index_end = script_with_data.find("}]}]") + len("}]}]")
data = script_with_data[data_index_start:data_index_end]

with open('frigidair_data.json', 'w') as outfile:
    outfile.write(data)