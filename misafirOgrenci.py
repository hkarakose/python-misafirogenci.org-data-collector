import time

import requests
import json
from bs4 import BeautifulSoup
import re
import pandas as pd
import openpyxl

def fetch(data_input):
	global response
	url = "https://www.misafirogrenci.org/ajax/get-data.php"
	headers = {
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"Accept": "*/*",
		"X-Requested-With": "XMLHttpRequest"
	}

	time.sleep(0.5)
	return requests.post(url, headers=headers, data=data_input)


x = {
	"request": "fill-map"
}

response = fetch(data_input=x)

# print(response.text)
x = json.loads(response.text)
cities = x["response"]["data"]
# print(cities)

excel_data = []

for c in cities:
  # print(c)
  x = {
    "request": "okullar-table",
    "s": c["il"]
  }
  response = fetch(data_input=x)
  # print(response.text)
  x=json.loads(response.text)

  html_ = x["html"].replace("\n", "")
  soup = BeautifulSoup(html_, 'html.parser')
  for tr in soup.find_all('tr'):
    cells = tr.find_all('td')
    if cells:
      school = cells[0].text
      city = cells[1].text
      count = cells[2].text.replace(" - DETAY", "")
      print(f'{school}, {city}, {count}')
      excel_data.append([school, city, count])


df = pd.DataFrame(excel_data, columns=['School', 'City', 'Count'])
df_sorted=df.sort_values("Count")
df_sorted.to_excel('data.xlsx', index=False)