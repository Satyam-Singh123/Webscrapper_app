import os

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app = Flask(__name__)


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/quote', methods=['POST', 'GET'])  # route to show the review comments in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")
            site_url = 'http://quotes.toscrape.com/tag/' + searchString.lower() + '/'
            uClient = uReq(site_url)
            site_page = uClient.read()
            uClient.close()
            scrap_html = bs(site_page, "html.parser")

            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Author, Quote \n"
            fw.write(headers)
            #reviews = []
            quotes = []


            for data in scrap_html.find_all('div', {'class': 'quote'}):
                quotes.append({'Author': str(data.small.text), 'Quote': str(data.span.text)})

            return render_template('results.html', Quotes=quotes[0:(len(quotes) - 1)])

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    else:
        return render_template('index.html')

port = int(os.getenv("PORT"))
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=port)
