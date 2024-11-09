import os

from common.constant import action_env, scavenge_action
from common.util import load_config
from scavenge.scavenge import execute_scavenge

config = load_config('resources/config.yaml')

if __name__ == '__main__':
    action = os.getenv(action_env)
    if action == scavenge_action:
        execute_scavenge(config)
    else:
        print("unknown action")
