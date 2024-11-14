import os

from common.constant import action_env, scavenge_action, loot_action
from common.util import load_config
from loot.loot_service import execute_loot
from scavenge.scavenge_scheduler import schedule_scavenge

config = load_config('resources/config.yaml')

if __name__ == '__main__':
    action = os.getenv(action_env)
    if action == scavenge_action:
        schedule_scavenge(config)
    elif action == loot_action:
         execute_loot(config)
    else:
        print("unknown action")