import os
import time
import re

import requests
from flask import Flask, request

app = Flask(__name__)

last_token = {
    'token_type': 'Bearer',
    'expires_in': 259200,
    'expires': 0,
    'access_token': '',
    'refresh_token': '',
    'status': 'success'
}


def log_in():
    global last_token
    now = time.time()
    if now > last_token["expires"]:
        print('fetch new token')
        url = "https://www.minds.com/api/v2/oauth/token"

        querystring = {"cb": f'{now}'}

        payload = {
            "grant_type": "password",
            "client_id": "mobile",
            "username": os.environ['MINDS_USERNAME'],
            "password": os.environ['MINDS_PASSWORD']
        }

        headers = {
            'app-version': "4.1.2",
            'content-type': "application/json",
            'user-agent': "okhttp/3.12.1"
        }

        response = requests.request("POST", url, json=payload, headers=headers, params=querystring)
        last_token = response.json()
        last_token["expires"] = now + last_token["expires_in"] * 1000
    return last_token["access_token"]


def un_shorten(url):
    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True)
    return resp.url


def get_url_in_text(text):
    found = re.search("(?P<url>https?://[^\s]+)", text)
    if found is None:
        return None
    else:
        return found.group("url")


def extract_hash_tags(s):
    return set(part[1:] for part in s.split() if part.startswith('#'))


@app.route('/post', methods=['POST'])
def post():
    url = "https://www.minds.com/api/v1/newsfeed"
    content = request.json
    message = content["text"]
    hash_tags = extract_hash_tags(message)
    url_in_text = get_url_in_text(message)
    if url_in_text is not None:
        message = message.replace(url_in_text, un_shorten(url))

    payload = {
        "message": message,
        "wire_threshold": None,
        "paywall": False,
        "time_created": None,
        "mature": False,
        "nsfw": [],
        "tags": list(hash_tags),
        "access_id": "2",
        "license": "all-rights-reserved"
    }

    token = log_in()
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache, no-store, must-revalidate",
        'pragma': "no-cache",
        'app-version': "4.1.2",
        'authorization': f"Bearer {token}"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    post_status = response.json()["status"]
    print(post_status, content["text"])
    return post_status


if __name__ == '__main__':
    app.run()
