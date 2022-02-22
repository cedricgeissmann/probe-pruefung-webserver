# import necessary modules
from bs4 import BeautifulSoup
import requests
import json


# get the URL in a useable form
url = "https://www.w3schools.com/cssref/css_selectors.asp"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# select your objects
table_rows = [elem for elem in soup.select('.ws-table-all tr')]


# define filter function
def filter_func(elem):
    return True

# apply filter function                  #wie man filter anwendet
table_rows = list(filter(filter_func, table_rows))


# create the structure for the json file
selectors = []                           #Resultat das geschirben werden soll (Liste)

for row in table_rows:
    cells = list(row.select('td'))
    if cells:                             #Falls Zelle vorhanden ist
        entry = {
            'selector': "placeholder text, which will be overwritten below",
            'example': cells[1].text,
            'description': cells[2].text,
            
        }
        # we need the following code beacause not all entries in the first column are text - some are links (a-tag)
        if cells[0].a:
            entry['selector'] = cells[0].a.text              #Wenn es a hat (internet Tabelle)
        else:
            entry['selector'] = cells[0].text               #Falls kein a dann nur der Text

        selectors.append(entry)
        

with open("selectors.json", 'w') as f:                        #Zeiel unten einschreiben nach f
    json.dump(selectors, f, indent=4)
