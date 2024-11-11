from common.util import load_config
from loot.extractor import initialize_loot_credentials, get_loot_ch_value
from loot.loot_client import send_loot_request


def execute_loot(config):
    loot_config = load_config('resources/loot_config.yaml')
    for loot in loot_config:
        village_id = loot["villageId"]
        name, value = initialize_loot_credentials(config, village_id, 18273)
        print(name)
        print(value)

        target = {
            "x": "408",
            "y": "563"
        }

        ch = get_loot_ch_value(config, village_id, name, value, target)
        send_loot_request(config, village_id, target, ch)
