import threading
import time
import logging

class Heartbeat(threading.Thread):
    def __init__(self, connection):
        super(Heartbeat, self).__init__()
        self.lock = threading.Lock()
        self.connection = connection
        self.setDaemon(True)
        self.quit_flag = False
        self.stop_flag = True

    def run(self):
        while not self.quit_flag:
            time.sleep(45)
            self.lock.acquire()
            if self.stop_flag:
                self.lock.release()
                continue
            try:
                self.connection.process_data_events()
            except Exception as e:
                logging.warn("Error format: %s" % str(e))
                self.lock.release()
                return
            self.lock.release()

    def startHeartbeat(self):
        self.lock.acquire()
        if self.quit_flag:
            self.lock.release()
            return
        self.stop_flag = False
        self.lock.release()
