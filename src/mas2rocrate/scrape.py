import requests


def make_auth_headers(username, token):
    return {
        "Authorization": f"Bearer {token}",
        "Username": username,
    }


def get_all(endpoint, username, token):
    headers = make_auth_headers(username, token)
    r = requests.get(endpoint, headers=headers)
    return r.json()
