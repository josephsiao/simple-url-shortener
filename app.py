from configparser import ConfigParser

from flask import Flask, render_template, request

from pg_database import PostgreDB
from short_url_generator import URLShortener

app = Flask(__name__)

config = ConfigParser()
config.read('config.ini')

DOMAIN_NAME = config['MAIN']['DomainName']
LENGTH = config['MAIN']['Length']
PROTOCOL = config['MAIN']['Protocol']
DB = dict([list(x) for x in config['DATABASE'].items()])

URL_SHORTENER = URLShortener(length=LENGTH)
POSTGRE_DB = PostgreDB(DB)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.values['url']
        short_url = URL_SHORTENER.short(url)

        POSTGRE_DB.add_data((short_url, url))

        return PROTOCOL + '://' + DOMAIN_NAME + '/' + short_url
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
