# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import queue
from src.threading.worker_thread import *
from src.threading.worker_state import WorkerState


class ThreadManager:
    """Has instance of work threads, manages communications between them
    and the classes that would interact with LogMessage data.
    """

    def __init__(self):
        """Initialize class members

        """
        self.interval = 50 # how many ms between queue checks
        self.feedback_log = queue.Queue()  # holds messages for log
        self.worker_thread = None

    def has_message_available(self):
        return not self.feedback_log.empty()

    def get_message(self):
        message = self.feedback_log.get(block=True)
        self.feedback_log.task_done()
        return message

    def pause_work(self):
        if self.worker_thread is not None:
            self.worker_thread.change_state(WorkerState.PAUSE)

    def kill_work(self):
        if self.worker_thread is not None:
            self.worker_thread.kill()
            self.worker_thread = None


    def start_work(self):
        self.worker_thread = WorkerThread(self.feedback_log)  # only created when processing begins. May be recreated
        self.worker_thread.daemon = True
        self.worker_thread.start()

    def continue_work(self):
        if self.worker_thread is not None:
            self.worker_thread.change_state(WorkerState.RUNNING)


