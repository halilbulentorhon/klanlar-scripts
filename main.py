from common.util import load_config
from scavenge.scavenge import execute_scavenge

config = load_config('resources/config.yaml')

if __name__ == '__main__':
    execute_scavenge(config)
