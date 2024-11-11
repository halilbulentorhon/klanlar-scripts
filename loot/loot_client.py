import requests

from common.util import get_base_request_headers, get_csrf_token


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
        "spear": "1",
        "sword": "0",
        "axe": "0",
        "archer": "0",
        "spy": "0",
        "light": "0",
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

    print(response.text)
