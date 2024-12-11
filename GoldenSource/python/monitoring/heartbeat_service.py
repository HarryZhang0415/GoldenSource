import datetime
import requests
from threading import Thread
import time
from GoldenSource.python.common.services import Service

class HeartBeatMonitoringService(Service):

    UAT_SERVICE_URL = 'xxxx' #TO-DO
    PROD_SERVICE_URL = 'xxxx' #TO-DO

    def __init__(self, domain) -> None:
        self.domain = domain
        self.logger = self.domain.logger_service.get_logger()
        self._processes = []

        if self.domain.configuration.disable_hb:
            self.logger.info('Heartbeat monitoring is disabled')
            return
        
        self._interval = self.domain.configuration.hb_interval
        self._shut_off = False

        self.env = self.domain.get_param("environment")
        if self.env == 'UAT':
            self.service_url = self.UAT_SERVICE_URL
        else:
            self.service_url = self.PROD_SERVICE_URL

        self.run_async = self.domain.get_param('app', 'run_async', default=True)

        if self.run_async:
            self.logger.info(
                'Starting heartbeat monitoring process to {} at interval {}'.format(self.service_url, self._interval))
            self.trigger = Thread(target=self._submit_heartbeat_by_job_name)
            self.trigger.start()
    
    def _submit_heartbeat_by_job_name(self):
        while not self._shut_off:
            for name in self._processes:
                payload = {'Name': name, "LastUpdated": '{}'.format(datetime.datetime.now())}
                self._send_request(payload)
            time.sleep(self._interval)
    
    def _send_request(self, payload):
        try:
            response = requests.put(self.service_url, data=payload, timeout=5)
            if response.status_code == 200:
                self.logger.info('Heartbeat sent successfully')
            else:
                self.logger.error('Failed to send heartbeat')
        except Exception as e:
            self.logger.error('Failed to send heartbeat to site {}: {}'.format(self.service_url, e))
        
    def send_oneoff_request(self, name):
        payload = {'Name': name, "LastUpdated": '{}'.format(datetime.datetime.now())}
        self._send_request(payload)

    def add_process_to_heartbeat(self, job):
        if job not in self._processes:
            self._processes.append(job)
    
    def remove_process_from_heartbeat(self, job):
        try:
            self._processes.remove(job)
        except Exception as e:
            self.logger.error('Job {} failed to remove process from heartbeat: {}'.format(job, e))
    
    def shutdown(self):
        self.logger.info('Shutting down heartbeat monitoring service')
        self._shut_off = True