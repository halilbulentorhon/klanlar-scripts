import os

from common.constant import action_env, scavenge_action
from common.util import load_config
from loot.loot_service import execute_loot
from scavenge.scavenge_scheduler import schedule_scavenge

config = load_config('resources/config.yaml')

if __name__ == '__main__':
    execute_loot(config)
    # action = os.getenv(action_env)
    # if action == scavenge_action:
    #     schedule_scavenge(config)
    # else:
    #     print("unknown action")
