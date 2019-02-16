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
from src.threading.test_job_A import TestJobA
from src.threading.test_job_B import TestJobB



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

        # Fill this list with whatever jobs need doing, in order
        self.job_list = [TestJobA(self.feedback_log).__class__,
                         TestJobB(self.feedback_log).__class__,]

    def has_message_available(self):
        """Checks if message queue is not empty

        :return: Boolean indicating if queue is not empty
        """
        return not self.feedback_log.empty()

    def get_message(self):
        """Get log message off feedback log queue

        :return: LogMessage that was taken from queue
        """
        message = self.feedback_log.get(block=True)
        self.feedback_log.task_done()
        return message

    def pause_work(self):
        """Change worker state to PAUSE

        :return: None
        """
        if self.worker_thread is not None:
            self.worker_thread.change_state(WorkerState.PAUSE)

    def kill_work(self):
        """Kill worker thread if it exists and set it to None

        :return: None
        """
        if self.worker_thread is not None:
            self.worker_thread.kill()
            self.worker_thread.join()
            self.worker_thread = None

    def start_work(self):
        """Create new worker thread and begin running it

        :return: None
        """
        self.worker_thread = WorkerThread(self.feedback_log, self.job_list)  # only created when processing begins. May be recreated
        self.worker_thread.daemon = True
        self.worker_thread.start()

    def continue_work(self):
        """Change worker state to RUNNING

        :return: None
        """
        if self.worker_thread is not None:
            self.worker_thread.change_state(WorkerState.RUNNING)


