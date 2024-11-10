import requests
import re
import json

from common.util import get_base_request_headers


def get_village_data(config, village_id):
    url = f"{config['gameInfo']['baseUrl']}/game.php?village={village_id}&screen=place&mode=scavenge"
    headers = get_base_request_headers(config, village_id, "main")

    response = requests.get(url, headers=headers)

    match = re.search(r'var village = ({.*?});', response.text)
    if match:
        village_data = match.group(1)

        try:
            village_obj = json.loads(village_data)
            return village_obj
        except json.JSONDecodeError as e:
            print("json parse error while extracting village data: ", e)
            return None
    else:
        print("could not find village data in content")
        return None
