import time

import requests
import json

from common.util import get_base_request_headers, get_csrf_token


def post_scavenge(config, village_id, option_id, troops):
    data = {
        "squad_requests[0][village_id]": str(village_id),
        "squad_requests[0][candidate_squad][unit_counts][spear]": str(troops["Sp"]),
        "squad_requests[0][candidate_squad][unit_counts][sword]": str(troops["Sw"]),
        "squad_requests[0][candidate_squad][unit_counts][axe]": "0",
        "squad_requests[0][candidate_squad][unit_counts][archer]": "0",
        "squad_requests[0][candidate_squad][unit_counts][light]": "0",
        "squad_requests[0][candidate_squad][unit_counts][marcher]": "0",
        "squad_requests[0][candidate_squad][unit_counts][heavy]": "0",
        "squad_requests[0][candidate_squad][unit_counts][knight]": "0",
        "squad_requests[0][candidate_squad][carry_max]": "0",
        "squad_requests[0][option_id]": str(option_id),
        "squad_requests[0][use_premium]": "false",
        "h": get_csrf_token(config, village_id)
    }

    url = (f"{config['gameInfo']['baseUrl']}/game.php?village={str(village_id)}&screen=scavenge_api&"
           f"ajaxaction=send_squads")

    response = requests.post(url, headers=get_base_request_headers(config, str(village_id), "place"), data=data)

    response_data = json.loads(response.text)

    if response_data["response"]["squad_responses"][0]["success"]:
        print(f"scavenge request successfully sent to option ({option_id}), with troops {troops}")
    else:
        print("scavenge request failed for reason: ", response_data["response"]["squad_responses"][0]["error"])

    time.sleep(100)
