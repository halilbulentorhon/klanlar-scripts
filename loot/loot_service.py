import math
import time
import requests
from common.util import load_config
from loot.extractor import initialize_loot_credentials, get_loot_ch_value
from loot.loot_client import send_loot_request,get_close_vilages


def send_loot(config,targetId,target):
    loot_config = load_config('resources/loot_config.yaml')
    for loot in loot_config:
        village_id = loot["villageId"]
        name, value = initialize_loot_credentials(config, village_id, targetId)

        ch = get_loot_ch_value(config, village_id, name, value, target)
        send_loot_request(config, village_id, target, ch)

def convert_minutes_to_hours(minutes):
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"

def getBarbarianVillages():
    village_position = {
            "x": 416,
            "y": 570
        }
    all_villages = get_close_vilages()
    barbar_villages = []
    for map_view_port in all_villages:
        villages = map_view_port["data"]["villages"]
        x = int(map_view_port["data"]["x"])
        y = int(map_view_port["data"]["y"])

        if not isinstance(villages, list):
            for key, value in villages.items():
                if isinstance(value, list) and len(value) > 2 and value[2] == 0:
                    distance = math.sqrt((x + int(key) - village_position["x"]) ** 2 +
                                         (int(key) - village_position["y"]) ** 2)
                    barbar_villages.append({
                        "x": x + int(key),
                        "y": y,
                        "distance": distance,
                        "target": value[0],
                        "time": convert_minutes_to_hours(int(distance * 10)),
                        "minutes": math.ceil(distance * 10),
                    })

                elif not isinstance(value, list):
                    for key2, value2 in value.items():
                        if value2[2] == 0:
                            distance = math.sqrt((x + int(key) - village_position["x"]) ** 2 +
                                                 (y + int(key2) - village_position["y"]) ** 2)
                            barbar_villages.append({
                                "x": x + int(key),
                                "y": y + int(key2),
                                "distance": distance,
                                "target": value2[0],
                                "time": convert_minutes_to_hours(int(distance * 10)),
                                "minutes": math.ceil(distance * 10),
                            })

        elif isinstance(villages, list):
            for index, village in enumerate(villages):
                if isinstance(village, list):
                    for i, a in enumerate(village):
                        if a[2] == 0:
                            distance = math.sqrt((x + index - village_position["x"]) ** 2 +
                                                 (y + i - village_position["y"]) ** 2)
                            barbar_villages.append({
                                "x": x + index,
                                "y": y + i,
                                "distance": distance,
                                "target": a[0],
                                "time": convert_minutes_to_hours(int(distance * 10)),
                                "minutes": math.ceil(distance * 10),
                            })

                elif not isinstance(village, list):
                    for key2, value2 in village.items():
                        if value2[2] == 0:
                            distance = math.sqrt((x + index - village_position["x"]) ** 2 +
                                                 (y + int(key2) - village_position["y"]) ** 2)
                            barbar_villages.append({
                                "x": x + index,
                                "y": y + int(key2),
                                "distance": distance,
                                "target": value2[0],
                                "time": convert_minutes_to_hours(int(distance * 10)),
                                "minutes": math.ceil(distance * 10),
                            })

    return sorted(barbar_villages, key=lambda k: k["distance"])

def add_minutes_to_millis(minutes):
    return int(time.time() * 1000) + (minutes * 60000)


def execute_loot(config):
   
    barbar = getBarbarianVillages()
    new_barbar = [{**village, "finishTime": 0} for village in barbar]
    while True:
        for village in new_barbar:
            if village["finishTime"] < int(time.time() * 1000):  # Check if finishTime is in the past
                try:
                    # Make a POST request with the village's data
                    target = {
                        "x": village["x"],
                        "y": village["y"]
                    }
                    send_loot(config, village["target"],target)

                    # Update finishTime after the request is successful
                    village["finishTime"] = add_minutes_to_millis(village["minutes"])
                    print("sent:", village["x"], village["y"],'distance: ',village["distance"])

                except requests.RequestException as error:
                    print("Request failed for village:", village["x"], village["y"], error)
                except Exception as e:
                    if str(e) == "Yeterli birim yok":
                        break
                time.sleep(3)

        time.sleep(300) 

