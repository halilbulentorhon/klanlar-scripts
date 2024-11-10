from common.util import load_config
from scavenge.scavenge_calculator import calculate_troops
from scavenge.scavenge_client import post_scavenge
from scavenge.village_data import get_village_data


def execute_scavenge(config):
    scavenge_config = load_config('resources/scavenge_config.yaml')
    for scavenge in scavenge_config:
        village_id = scavenge["villageId"]
        village_data = get_village_data(config, village_id)
        scavenge_data = prepare_scavenge_data(scavenge, village_data)

        calculation = calculate_troops(scavenge_data)
        if calculation is not None:
            send_scavenge_request(config, village_id, calculation)


def send_scavenge_request(config, village_id, scavenge_calculation):
    if is_scavenge_satisfied(scavenge_calculation, "FF"):
        post_scavenge(config, village_id, 1, scavenge_calculation["FF"])
    if is_scavenge_satisfied(scavenge_calculation, "BB"):
        post_scavenge(config, village_id, 2, scavenge_calculation["BB"])
    if is_scavenge_satisfied(scavenge_calculation, "SS"):
        post_scavenge(config, village_id, 3, scavenge_calculation["SS"])
    if is_scavenge_satisfied(scavenge_calculation, "RR"):
        post_scavenge(config, village_id, 4, scavenge_calculation["RR"])


def prepare_scavenge_data(scavenge, village_data):
    ff_data = village_data["options"]["1"]
    bb_data = village_data["options"]["2"]
    ss_data = village_data["options"]["3"]
    rr_data = village_data["options"]["4"]
    scavenge_options = scavenge["options"]

    return {
        'maxHours': scavenge["maxHours"],
        'worldSpeed': scavenge["worldSpeed"],
        'spearCount': village_data["unit_counts_home"]["spear"],
        'swordCount': village_data["unit_counts_home"]["sword"],
        'options': {
            'ff': ff_data["is_locked"] is False and ff_data["scavenging_squad"] is None and scavenge_options[
                "ff"] is True,
            'bb': bb_data["is_locked"] is False and bb_data["scavenging_squad"] is None and scavenge_options[
                "bb"] is True,
            'ss': ss_data["is_locked"] is False and ss_data["scavenging_squad"] is None and scavenge_options[
                "ss"] is True,
            'rr': rr_data["is_locked"] is False and rr_data["scavenging_squad"] is None and scavenge_options[
                "rr"] is True
        }
    }


def is_scavenge_satisfied(calculation, key):
    spear_count = calculation[key]["Sp"]
    sword_count = calculation[key]["Sw"]

    if spear_count + sword_count > 10:
        return True
    return False
