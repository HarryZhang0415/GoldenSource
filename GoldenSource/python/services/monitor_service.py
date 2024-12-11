from collections import defaultdict

from threading import RLock
from GoldenSource.python.common.services import Service


class MonitorService(Service):
    """
    MonitorService monitors a set of jobs and subsequently runs one or more triggers following the completion 
    of all the jobs.
    """
    def __init__(self, domain):
        super(MonitorService, self).__init__(domain)
        self._domain = domain
        self._logger = domain.logger_service.get_logger(self.__class__.__name__)
        self._triggers = defaultdict(set)
        self._triggers_lock = defaultdict(RLock)
        self._monitors = defaultdict(set)
        self._monitors_lock = defaultdict(RLock)

    def add_trigger(self, monitor_id, trigger):
        with self._triggers_lock[monitor_id]:
            self._triggers[monitor_id].add(trigger)

    def remove_trigger(self, monitor_id, trigger):
        with self._triggers_lock[monitor_id]:
            self._triggers[monitor_id].add(trigger)

    def monitor(self, monitor_id, jobs):
        with self._monitors_lock[monitor_id]:
            self._monitors[monitor_id].add(jobs)

    def monitor_all(self, monitor_id, jobs):
        with self._monitors_lock[monitor_id]:
            self._monitors[monitor_id].update(jobs)

    def _on_jobs_done(self, monitor_id):
        with self._triggers_lock[monitor_id]:
            for trigger in self._triggers[monitor_id]:
                try:
                    trigger.trigger(self._domain)
                except:
                    self._logger.exception("Error while triggering {!s} marking the end of {!s}".format(trigger, monitor_id))
                else:
                    self._logger.info("Trigger {!s} successfully executed marking the end of {!s}".format(trigger, monitor_id))
    
    def job_done(self, monitor_id, job):
        with self._monitors_lock[monitor_id]:
            try:
                self._logger.debug('{} completed'.format(job))
                self._monitors[monitor_id].remove(job)
            except KeyError:
                self._logger.warn('{} has already finished'.format(job))
            except:
                self._logger.exception('Error while removing {} from the monitor'.format(job))
            finally:
                if not self._monitors[monitor_id]:
                    self._on_jobs_done(monitor_id)