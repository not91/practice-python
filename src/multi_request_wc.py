import requests
from requests import exceptions as requests_exc
from concurrent.futures import ThreadPoolExecutor, as_completed
import re


def worker(url, search_string):
    try:
        text = requests.get(url, timeout=5).text
        words = re.findall(search_string, text)
        return {url: len(words)}
    except (requests_exc.HTTPError,
            requests_exc.ConnectTimeout, requests_exc.RequestException) as err:
        return {url: None}
    except Exception:
        print(err)


def run(urls, search_string, max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        results = []
        for url in urls:
            results.append(pool.submit(worker, url, search_string))

        return as_completed(results)


if __name__ == "__main__":

    urls = [
        'https://pravo.ru',
        'https://ria.ru',
        'https://lenta.ru',
        'https://news.rambler.ru',
        'https://news.yandex.ru'
    ]

    result = run(urls, 'yandex', max_workers=3)

    for future in result:
        print(future.result())
