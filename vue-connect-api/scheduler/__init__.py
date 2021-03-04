from apscheduler.schedulers.background import BackgroundScheduler

from backend.routes import info
from common import config


logger = config.get_logger("scheduler")


class Scheduler:
    def __init__(self):
        self._scheduler = BackgroundScheduler(daemon=True)

    def add_job(self, job):
        # add job
        if job.get_poll_intervall() > 0:
            logger.info("register job {}".format(type(job)))
            self._scheduler.add_job(
                func=job.run,
                trigger="interval",
                seconds=job.get_poll_intervall(),
            )

    def start(self):
        self._scheduler.start()

    def shutdown(self):
        logger.info("stopping scheduler")
        self._scheduler.shutdown()
