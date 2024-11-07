import requests
import json

from common.util import get_base_request_headers, get_csrf_token, load_config


def execute_scavenge(config):
    commands = load_config("resources/scavenge_commands.yaml")['commandList']

    for command in commands:
        village_id = command['villageId']
        option_id = command['option']
        units = command['units']

        data = {
            "squad_requests[0][village_id]": str(village_id),
            "squad_requests[0][candidate_squad][unit_counts][spear]": str(units.get("spear", 0)),
            "squad_requests[0][candidate_squad][unit_counts][sword]": str(units.get("sword", 0)),
            "squad_requests[0][candidate_squad][unit_counts][axe]": str(units.get("axe", 0)),
            "squad_requests[0][candidate_squad][unit_counts][archer]": str(units.get("archer", 0)),
            "squad_requests[0][candidate_squad][unit_counts][light]": str(units.get("light", 0)),
            "squad_requests[0][candidate_squad][unit_counts][marcher]": str(units.get("marcher", 0)),
            "squad_requests[0][candidate_squad][unit_counts][heavy]": str(units.get("heavy", 0)),
            "squad_requests[0][candidate_squad][unit_counts][knight]": str(units.get("knight", 0)),
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
            print("scavenge request successfully sent")
        else:
            print("scavenge request failed for reason: ", response_data["response"]["squad_responses"][0]["error"])
