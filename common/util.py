import yaml
import requests
import re


def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def read_cookie():
    with open('resources/cookie.txt', 'r') as file:
        return file.read()


def get_base_request_headers(config, village_id, screen):
    headers = config["baseRequest"]["headers"]
    headers["origin"] = config["gameInfo"]["baseUrl"]
    headers["cookie"] = read_cookie()
    headers["referer"] = f"{config['gameInfo']['baseUrl']}/game.php?village={village_id}&screen={screen}"
    return headers


def get_csrf_token(config, village_id, screen="overview"):
    url = f"{config['gameInfo']['baseUrl']}/game.php?village={village_id}&screen={screen}"
    headers = get_base_request_headers(config, village_id, "main")

    response = requests.get(url, headers=headers)

    match = re.search(r"var csrf_token = '([^']+)'", response.text)

    if match:
        csrf_token = match.group(1)
        return csrf_token
    else:
        print("could not find csrf_token")
        return None
