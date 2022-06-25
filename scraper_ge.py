import requests, re, json
from bs4 import BeautifulSoup

session = requests.Session()

looping_through_pages = True
page_count = 0
product_data = []

while looping_through_pages == True:

  URL = "https://www.geappliances.ca/products/category/Refrigerators?query=&sort_by=price&sort_order=DESC&page=" + str(page_count)

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

  results = soup.find_all("div", class_="views-row")

  if len(results) > 0:

    for result in results:
      product_url = result.a['href']
      product_img_url = 'https://www.geappliances.ca' + result.img['src']
      product_code = result.img['src']
      product_id = result.find("div", class_="field sku field--type-string field--label-visually_hidden").text
      product_name = result.find("div", class_="field title field--type-string field--label-visually_hidden").contents[3].text
      product_price = result.article.contents[5].contents[1].div.contents[0].strip()
      product = {"product_url": product_url, "product_img_url": product_img_url, "product_code": product_code, "product_id": product_id, "product_name": product_name, "product_price": product_price}
      product_data.append(product)

    page_count += 1
  else:
    looping_through_pages = False

with open('ge_data.json', 'w') as outfile:
    json.dump(product_data, outfile)