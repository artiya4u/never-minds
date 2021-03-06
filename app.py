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

        querystring = {"cb": f'{int(now * 1000)}'}

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
        last_token["expires"] = now + last_token["expires_in"]
    return last_token["access_token"]


def un_shorten(url):
    session = requests.Session()  # so connections are recycled
    resp = session.head(url, allow_redirects=True)
    return resp.url


def get_url_in_text(text):
    return re.findall("(?P<url>https?://[^\s]+)", text)


def extract_hash_tags(s):
    return set(part[1:] for part in s.split() if part.startswith('#'))


@app.route('/post', methods=['POST'])
def post():
    url = "https://www.minds.com/api/v1/newsfeed"
    print(request.data)
    content = request.json
    message = content["text"]
    hash_tags = extract_hash_tags(message)
    urls_in_text = get_url_in_text(message)
    if len(urls_in_text) > 0:
        for u in urls_in_text:
            message = message.replace(u, un_shorten(u))

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
    print(post_status, message)
    return post_status


if __name__ == '__main__':
    app.run()
