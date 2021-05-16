#!venv/bin/python
from bs4 import BeautifulSoup as Soup
import logging
import requests
import sys
import webbrowser


def main(postcode: str):
    logger = get_logger()
    url = f'https://www.prullenbakvaccin.nl/{postcode}'

    response = requests.get(url, headers={
        'accept': '*/*',
        'accept-language': 'nl-NL,nl;q=0.9,en-NL;q=0.8,en;q=0.7,en-US;q=0.6',
        'authority': 'www.prullenbakvaccin.nl',
        'cookie': "XSRF-TOKEN=eyJpdiI6IjN3TWZVNTdqcVZFeEZyWXFiVkc1UkE9PSIsInZhbHVlIjoiSHRtaHZUZklDSE04THNCV2hjeVJkdnhOdVdKdXpOOWxEQ3I0dDdBbS9GdjNPZEkrL2JOVlFhU1FOZnJNMVprMFJtWitSQ1B6Mk8rZTlRYnVsc2tyMFpHbm11OElUVlc5VWRJMjBLVXJHZTY3cldVTERON3d6V0RsQWJEaUJocDMiLCJtYWMiOiI2YTg5OWIyOGVjN2MxYmEwYzMyMWJiM2E4NmIxNzBlYWY2ZjJjZTVjODQ3ZmRkNGY0Njc4ODJkODQwNjJiZDJjIn0%3D; prullenbakvaccin_session=eyJpdiI6Ik1Ha3NOdUhPY05RU0lxenRCQ2kzaUE9PSIsInZhbHVlIjoiNk9DYzhHN2JMSTg3TDRCaXVCS2ZXZEFDOXJnR0xSTlhvbDBxNGN5N1lDQUpOUVUxSkY3QnRkOWo3WkIxSjlROXUvUklsWnR0SlZHRURxanI4QkQyVElGSlp0Zi9nN0Z5Y2xMa2h5YU01T2ZBcXRQSGxndkxoMm5laDYvMGVzRG8iLCJtYWMiOiJkZWU3YmE0NmQ4M2ZlZTE3NWUxYWI3MzM1ODdkNzdiZmNiZTQzOTJhZDhkOWU0NGIwY2E1NzMwMzNmYTUzMTk3In0%3D",
        'dnt': '1',
        'referer': f'https://www.prullenbakvaccin.nl/{postcode}',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
        'x-csrf-token': 'dTUCryo9Qi8YvcjZUkuMciHmWKZbNh6SR3s1ek6J',
        'x-requested-with': 'XMLHttpRequest',
    })

    content = response.content.decode('utf-8')
    soup = Soup(content, features="html.parser")
    card_titles = soup.select("#locations-container>div .card-title")
    smalls = [item.find('small').contents[0] for item in card_titles]
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

    found_one = False
    for item in smalls:
        if 'geen vaccins' not in item:
            found_one = True

    if found_one:
        logger.info(f"hebbes! {postcode}")
        webbrowser.get(chrome_path).open(url)

        sys.exit(0)
    else:
        logger.debug(f"geen vaccins :( {postcode}")
        sys.exit(1)


def get_logger() -> logging.Logger:
    logger = logging.getLogger('prullenbakvaccin')
    handler = logging.FileHandler("prullenbakvaccin.log")
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger


if __name__ == '__main__':
    main(sys.argv[1])
