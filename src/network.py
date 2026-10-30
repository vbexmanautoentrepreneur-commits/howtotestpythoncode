import requests


def get_status(url):
    return requests.get(url).status_code