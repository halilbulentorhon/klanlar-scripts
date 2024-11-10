import math
import json


def cp(o):
    return json.loads(json.dumps(o))


def do_try_move_from_raid1_to_raid2(i_cap, r, i_change, i_raid1, i_raid2, i_max_duration, data):
    if i_raid1 == i_raid2:
        return r
    i_unchanged = get_loss_function_output(i_cap, r, i_max_duration, data)

    r_changed = cp(r)
    if i_change > r_changed[i_raid2]:
        i_change = r_changed[i_raid2]
    r_changed[i_raid1] += i_change
    r_changed[i_raid2] -= i_change

    i_changed = get_loss_function_output(i_cap, r_changed, i_max_duration, data)
    if i_changed > i_unchanged:
        return r_changed
    else:
        return r


def fn_gain(i_cap, r, i_max_duration, data):
    i_max_cap = fn_duration_to_cap(i_max_duration, r, data)
    return {
        "FF": round(min(r[0] * i_cap, i_max_cap["FF"]) * 0.10),
        "BB": round(min(r[1] * i_cap, i_max_cap["BB"]) * 0.25),
        "SS": round(min(r[2] * i_cap, i_max_cap["SS"]) * 0.50),
        "RR": round(min(r[3] * i_cap, i_max_cap["RR"]) * 0.75)
    }


def get_duration_factor(data):
    return math.pow(data["worldSpeed"] * 1, -0.55)


def fn_duration_to_cap(i_duration, r, data):
    if i_duration == float('inf'):
        return {"FF": float('inf'), "BB": float('inf'), "SS": float('inf'), "RR": float('inf')}

    return {
        "FF": 0 if r[0] == 0 else math.pow(
            math.pow((i_duration / get_duration_factor(data)) - 1800, 1 / 0.45) / math.pow(0.10, 2) / 100, 1 / 2),
        "BB": 0 if r[1] == 0 else math.pow(
            math.pow((i_duration / get_duration_factor(data)) - 1800, 1 / 0.45) / math.pow(0.25, 2) / 100, 1 / 2),
        "SS": 0 if r[2] == 0 else math.pow(
            math.pow((i_duration / get_duration_factor(data)) - 1800, 1 / 0.45) / math.pow(0.50, 2) / 100, 1 / 2),
        "RR": 0 if r[3] == 0 else math.pow(
            math.pow((i_duration / get_duration_factor(data)) - 1800, 1 / 0.45) / math.pow(0.75, 2) / 100, 1 / 2)
    }


def fn_duration(i_cap, r, i_max_duration, data):
    i_max_cap = fn_duration_to_cap(i_max_duration, r, data)
    return {
        "FF": 0 if r[0] == 0 else ((math.pow(math.pow(r[0] * min(i_cap, i_max_cap["FF"]), 2) * 100 * math.pow(0.10, 2),
                                             0.45) + 1800) * get_duration_factor(data)),
        "BB": 0 if r[1] == 0 else ((math.pow(math.pow(r[1] * min(i_cap, i_max_cap["BB"]), 2) * 100 * math.pow(0.25, 2),
                                             0.45) + 1800) * get_duration_factor(data)),
        "SS": 0 if r[2] == 0 else ((math.pow(math.pow(r[2] * min(i_cap, i_max_cap["SS"]), 2) * 100 * math.pow(0.50, 2),
                                             0.45) + 1800) * get_duration_factor(data)),
        "RR": 0 if r[3] == 0 else ((math.pow(math.pow(r[3] * min(i_cap, i_max_cap["RR"]), 2) * 100 * math.pow(0.75, 2),
                                             0.45) + 1800) * get_duration_factor(data))
    }


def fn_rph(i_cap, r, i_max_duration, data):
    o_duration = fn_duration(i_cap, r, i_max_duration, data)
    o_gain = fn_gain(i_cap, r, i_max_duration, data)
    return (
            (o_gain["FF"] / o_duration["FF"] if o_gain["FF"] != 0 else 0) +
            (o_gain["BB"] / o_duration["BB"] if o_gain["BB"] != 0 else 0) +
            (o_gain["SS"] / o_duration["SS"] if o_gain["SS"] != 0 else 0) +
            (o_gain["RR"] / o_duration["RR"] if o_gain["RR"] != 0 else 0)
    ) * 60 * 60


def get_loss_function_output(i_cap, r, i_max_duration, data):
    return fn_rph(i_cap, r, i_max_duration, data)


def get_optimal_distribution(r, i_cap, i_max_duration, a_raid_checked, data):
    i_iterations = 0
    i_current = get_loss_function_output(i_cap, r, i_max_duration, data)
    b_continue = True

    while b_continue:
        for raid_l in range(4):
            if not a_raid_checked[raid_l]:
                continue
            for raid_r in range(4):
                if not a_raid_checked[raid_r]:
                    continue
                i_change = r[raid_l] / 1.2
                for _ in range(10):
                    r = do_try_move_from_raid1_to_raid2(i_cap, r, i_change, raid_l, raid_r, i_max_duration, data)
                    i_change /= 1.2
                i_iterations += 1
        i_new = get_loss_function_output(i_cap, r, i_max_duration, data)
        if i_new > i_current:
            b_continue = True
            i_current = i_new
        else:
            b_continue = False
    return r, i_iterations


def calculate_troops(config):
    i_units = {
        "Sp": {"cap": 25, "cnt": config["spearCount"]},
        "Sw": {"cap": 15, "cnt": config["swordCount"]}
    }

    i_max_duration = (config["maxHours"] or 0) * 60 * 60
    if i_max_duration == 0:
        i_max_duration = float('inf')

    i_cap = i_units["Sp"]["cap"] * i_units["Sp"]["cnt"] + i_units["Sw"]["cap"] * i_units["Sw"]["cnt"]

    r = [7.5 if config["options"]["ff"] else 0, 3 if config["options"]["bb"] else 0,
         1.5 if config["options"]["ss"] else 0,
         1 if config["options"]["rr"] else 0]
    i_div = sum(r)
    if i_div == 0:
        return
    r = [x / i_div for x in r]

    r, _ = get_optimal_distribution(r, i_cap, i_max_duration,
                                    [config["options"]["ff"], config["options"]["bb"], config["options"]["ss"],
                                     config["options"]["rr"]], config)

    i_max_cap = fn_duration_to_cap(i_max_duration, r, config)
    i_caps = {
        "FF": round(min(i_max_cap["FF"], i_cap * r[0])),
        "BB": round(min(i_max_cap["BB"], i_cap * r[1])),
        "SS": round(min(i_max_cap["SS"], i_cap * r[2])),
        "RR": round(min(i_max_cap["RR"], i_cap * r[3]))
    }

    o_ret = {}

    def fn_fill(raid, unit):
        i_count = min(i_units[unit]["cnt"], math.floor(i_caps[raid] / i_units[unit]["cap"]))
        i_caps[raid] -= i_count * i_units[unit]["cap"]
        i_units[unit]["cnt"] -= i_count
        o_ret[raid][unit] = i_count

    def fn_fill_raid(raid):
        o_ret[raid] = {}
        fn_fill(raid, "Sp")
        fn_fill(raid, "Sw")

    fn_fill_raid("FF")
    fn_fill_raid("BB")
    fn_fill_raid("SS")
    fn_fill_raid("RR")

    return o_ret
