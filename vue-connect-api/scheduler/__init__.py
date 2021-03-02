import logging

from apscheduler.schedulers.background import BlockingScheduler


class Scheduler:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self._scheduler = BlockingScheduler(daemon=True)

    def add_job(self, job):
        # add job
        if job.get_poll_intervall() > 0:
            self._scheduler.add_job(
                func=job.run,
                trigger="interval",
                seconds=job.get_poll_intervall(),
            )

    def run(self):
        self._scheduler.start()
