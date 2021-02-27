from scheduler import Scheduler
from scheduler import job

if __name__ == "__main__":
    s = Scheduler()
    s.add_job(job.UpdateCacheJob())
    s.run()
