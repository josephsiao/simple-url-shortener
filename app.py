from flask import Flask, render_template, request

from short_url_generator import URLShortener
from configparser import ConfigParser

app = Flask(__name__)

config = ConfigParser()
config.read('config.ini')

DOMAIN_NAME = config['MAIN']['DomainName']
LENGTH = config['MAIN']['Length']
PROTOCOL = config['MAIN']['Protocol']
URL_SHORTENER = URLShortener(length=LENGTH)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.values['url']
        short_url = URL_SHORTENER.short(url)

        return PROTOCOL + '://' + DOMAIN_NAME + '/' + short_url
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
