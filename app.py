from configparser import ConfigParser

from flask import Flask, redirect, render_template, request

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
        url = request.values['url'].strip()
        short_url = POSTGRE_DB.check_data_exist(original=url)
        if not short_url:
            short_url = URL_SHORTENER.short(url)
            if not short_url:
                result = 'ValidationFailure. This may be an incorrect URL.'
            else:
                POSTGRE_DB.add_data((short_url, url))
                result = PROTOCOL + '://' + DOMAIN_NAME + '/' + short_url
        else:
            result = PROTOCOL + '://' + DOMAIN_NAME + '/' + short_url
        return render_template('index.html', url=url, result=result)
    else:
        return render_template('index.html')


@app.route('/<url>')
def url_redirect(url):
    result = POSTGRE_DB.check_data_exist(shorten=url)
    if result:
        return redirect(result)
    else:
        return 'PAGE DO NOT EXIST.'


if __name__ == '__main__':
    app.run(debug=True)
