import math
import time
import requests
import re
from common.util import load_config
from loot.extractor import initialize_loot_credentials, get_loot_ch_value
from loot.loot_client import send_loot_request,get_close_vilages
from common.util import get_base_request_headers
from datetime import datetime

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

def convert_and_adjust(data):
    result = []
    seen_pairs = set()

    for item in data:
        # Extract x and y values
        x, y = map(int, re.match(r'\((\d+)\|(\d+)\)', item).groups())
        
        # Adjust y if the pair already exists
        while (x, y) in seen_pairs:
            y -= 1  # Decrement y to make it unique
        
        # Add the unique (x, y) pair to the set and result list
        seen_pairs.add((x, y))
        result.append({"x": x, "y": y})

    return result

def loss_villages(config):
    village_position = {
            "x": 416,
            "y": 570
        }
    loot_config = load_config('resources/loot_config.yaml')
    for loot in loot_config:
        village_id = loot["villageId"]

    headers = get_base_request_headers(config, village_id, "report")
    url = f"https://tr89.klanlar.org/game.php?screen=report&mode=all&from=0&village={village_id}"
    response = requests.get(url, headers=headers)
    pattern = r"\(\d+\|\d+\)"

    matches = re.findall(pattern, response.text)
    print(re.match(r'\((\d+)\|(\d+)\)', matches[0]).groups())
    
    
    result = [{"x": int(x), "y": int(y)} for x, y in (re.match(r'\((\d+)\|(\d+)\)', item).groups() for item in matches)]

    filtered_result = [entry for entry in result if entry != village_position]
    return filtered_result

def remove_matched_elements(data, pairs_to_remove):
    remove_set = {(item["x"], item["y"]) for item in pairs_to_remove}
    
    filtered_data = [item for item in data if (item["x"], item["y"]) not in remove_set]
    
    return filtered_data


def execute_loot(config):

    barbar = getBarbarianVillages()
    new_barbar = [{**village, "finishTime": 0} for village in barbar]
    
    while True:
        loss = loss_villages(config)
        print(loss)
        current_time = datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")
        print("Current Time:", formatted_time)

        updated_new_barbar = remove_matched_elements(new_barbar, loss)
        for village in updated_new_barbar:
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

