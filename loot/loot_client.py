import requests
import json

from common.util import get_base_request_headers, get_csrf_token,load_config


def send_loot_request(config, village_id, target, ch):
    url = f"{config['gameInfo']['baseUrl']}/game.php?village={village_id}&screen=place&ajaxaction=popup_command"
    headers = get_base_request_headers(config, village_id, "map")

    form_data = {
        "attack": "true",
        "ch": ch,
        "cb": "troop_confirm_submit",
        "x": target['x'],
        "y": target['y'],
        "source_village": str(village_id),
        "village": str(village_id),
        "spear": "0",
        "sword": "0",
        "axe": "0",
        "archer": "0",
        "spy": "0",
        "light": "3",
        "marcher": "0",
        "heavy": "0",
        "ram": "0",
        "catapult": "0",
        "knight": "0",
        "snob": "0",
        "building": "main",
        "h": get_csrf_token(config, village_id=village_id, screen="map")
    }
   
    response = requests.post(url, headers=headers, data=form_data)
    expected_response = {'error': ['Geçersiz komut']}

# Parse the JSON response
    response_json = response.json()
    if response_json == expected_response:
        print('if girtdo')
        raise Exception("Yeterli birim yok")

def get_close_vilages():
    loot_config = load_config('resources/loot_config.yaml')
    for loot in loot_config:
        village_id = loot["villageId"]
        max_range = loot["maxRange"]

    village_position = {"x": 416, "y": 570}
    req_params = [f"{village_position['x']}_{village_position['y']}=0"]

    for i in range(20, max_range + 1, 20):
        req_params.append(f"{village_position['x']}_{village_position['y'] - i}=0")
        req_params.append(f"{village_position['x']}_{village_position['y'] + i}=0")
        req_params.append(f"{village_position['x'] - i}_{village_position['y']}=0")
        req_params.append(f"{village_position['x'] + i}_{village_position['y']}=0")

    url = f"https://tr89.klanlar.org/map.php?v=2&locale=tr_TR&e=1731262223893&{'&'.join(req_params)}"
    response = requests.get(url)
    return json.loads(response.text)

        ##send_loot_request(config, village_id, target, ch)