#import necessary modules
from flask import Flask, render_template
import json
from bs4 import BeautifulSoup                   #die vom scrape eingefügt das es Server finden kann
import requests


# set up flask webserver
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


def load_selectors():
    with open("selectors.json", 'r') as f:
        return json.load(f)


# webscraping function     
@app.route("/run-scraper")     #neu eingefügt               #der ganze rest kommt hier rein
def my_scraper():
# get the URL in a useable form
    url = "https://www.w3schools.com/cssref/css_selectors.asp"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # select your objects
    table_rows = [elem for elem in soup.select('.ws-table-all tr')]


    # define filter function                  #wird nicht mehr gebraucht
    def filter_func(elem):
        return True

    # apply filter function                  #wie man filter anwendet
    table_rows = list(filter(my_filter, table_rows))          #hier my filter eingesetzt 


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

            selectors.append(entry)                            #alles bis hier von scrape eingeführt
    write_json(selectors)     
    return "Scraping finished."                                 #eingefügt 


# filter function
def my_filter(elem):                                        #elem =element rein geschirben
    return True                                             # YOUR CODE GOES HERE
    

# output to json
def write_json(selectors):                                    #selectors rein geschrieben
 with open("selectors.json", 'w') as f:  
    json.dump(selectors, f, indent=4)                           # YOUR CODE GOES HERE
    


# define route(s)
@app.route("/")
def home():                                                  #Diese unten nochmal eingefügt
    return render_template("index.html")

# define route(s)
@app.route("/scraping")
def scraping():                                                #muss anderen Namen wie oben haben
    return render_template("scraping.html")                    #War Aufgabe 6


@app.route("/css-selectors")
def css_selectors():
    return render_template("css-selectors.html", selectors=load_selectors())


# starts the webserver
if __name__ == "__main__":
    app.run()
