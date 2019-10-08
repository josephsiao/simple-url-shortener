import base64
import hashlib
import logging

import validators


class URLShortener():
    """Shorten the URL."""
    length = 5

    def __init__(self, length):
        self.init_log()

    def short(self, url):
        """Hash the URL by md5 and base64, return shorter characters."""
        if validators.url(url):
            sha = hashlib.md5(url.encode('utf-8')).digest()
            altchars = '-_'.encode('utf-8')
            sha_base64 = base64.b64encode(sha, altchars).decode('utf-8')

            logging.info('URL: %s ===> %s', url, sha_base64[:self.length])
            return sha_base64[:self.length]
        else:
            logging.info('ValidationFailure. ===> %s', url)
            return None

    def init_log(self):
        """Init the logger."""
        FORMAT = '%(asctime)-20s %(levelname)-9s %(message)s'
        DATEFORMAT = '%Y-%m-%d %H:%M:%S'
        handler = logging.FileHandler('log.log', mode='a', encoding='utf-8')
        logging.basicConfig(handlers=[handler],
                            format=FORMAT,
                            datefmt=DATEFORMAT,
                            level=logging.INFO)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATEFORMAT))
        logging.getLogger().addHandler(console)
