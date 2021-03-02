from common import config
from scheduler import Scheduler
from scheduler import job
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    s = Scheduler()

    for cluster in config.get_connect_clusters():
        logging.info("register job for {}".format(cluster))
        s.add_job(job.UpdateCacheJob(cluster_id=cluster["id"]))

    s.run()
