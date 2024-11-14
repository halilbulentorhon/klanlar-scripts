import requests
import re

from common.util import get_base_request_headers


def initialize_loot_credentials(config, village_id, target):
    
    url = f"{config['gameInfo']['baseUrl']}/game.php?village={village_id}&screen=place&ajax=command&target={target}"
    headers = get_base_request_headers(config, village_id, "place")

    response = requests.get(url, headers=headers)

    data = response.json()
    html_content = data["response"]["dialog"]

    match = re.search(r'name="([^"]+)" value="([^"]+)"', html_content)

    name = match.group(1)
    value = match.group(2)

    return name, value


def get_loot_ch_value(config, village_id, name, value, target):
    url = f"{config['gameInfo']['baseUrl']}/game.php?village={village_id}&screen=place&ajax=confirm"
    headers = get_base_request_headers(config, village_id, "place")

    form_data = {
        name: value,
        "template_id": "",
        "source_village": str(village_id),
        "spear": "0",
        "sword": "0",
        "axe": "",
        "archer": "",
        "spy": "",
        "light": "3",
        "marcher": "",
        "heavy": "",
        "ram": "",
        "catapult": "",
        "knight": "",
        "snob": "",
        "x": target['x'],
        "y": target['y'],
        "target_type": "coord",
        "input": f"{target['x']}|{target['y']}",
        "attack": "l"
    }
  
    response = requests.post(url, headers=headers, data=form_data)
    data = response.json()
    expected_response = {"error": ["Yeterli birim yok"]}

# Parse the JSON response
    response_json = response.json()
    if response_json == expected_response:
        raise Exception("Yeterli birim yok")
    html_content = data["response"]["dialog"]

    match = re.search(r'<input[^>]*name="ch"[^>]*value="([^"]*)"', html_content)

    return match.group(1)
