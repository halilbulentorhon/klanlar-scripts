import sched
import time

from common.constant import scavenge_timer_interval
from scavenge.scavenge_service import execute_scavenge


def schedule_scavenge(config):
    scheduler = sched.scheduler(time.time, time.sleep)

    def run_scavenge(sc):
        execute_scavenge(config)
        sc.enter(scavenge_timer_interval, 1, run_scavenge, (sc,))

    scheduler.enter(0, 1, run_scavenge, (scheduler,))
    scheduler.run()
