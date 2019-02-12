# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import threading, time
from src.threading.worker_state import WorkerState
from src.log_messages.log_message import LogMessage
from src.log_messages.log_type import LogType


class WorkerThread(threading.Thread):
    """Thread for handling algorithms/processsing stuff
    """
    def __init__(self, feedback_log):
        threading.Thread.__init__(self)
        self.feedback_log = feedback_log
        self.state = WorkerState.RUNNING

    def run(self):
        """Process the thread and do work with its CPU time.

        :return: None
        """
        i = 1 # just test variable for test messages
        while self.state == WorkerState.RUNNING or self.state == WorkerState.PAUSE:
            while self.state == WorkerState.RUNNING:
                #do main stuff

                # testing messages
                self.put_feedback("Test message #" + str(i), LogType.INFORMATION)
                #print("test message " + self.feedback_log.get())
                i += 1
                time.sleep(0.5)

            while self.state == WorkerState.PAUSE:
                a = 1 + 1 # just spins...

    def put_feedback(self, msg, log_type):
        """

        :param msg:
        :param log_type:
        :return:
        """
        log_msg = LogMessage(log_type, msg)
        self.feedback_log.put(log_msg)

    def change_state(self, new_state):
        """Should stop/continue/pause this thread; throw error when appropriate

        :param new_state:
        :return:
        """
        self.state = new_state
        if new_state == WorkerState.RUNNING:
            self.put_feedback("Beginning processing.", LogType.DEBUG)
        elif new_state == WorkerState.PAUSE:
            self.put_feedback("Processing paused.", LogType.DEBUG)
        elif new_state == WorkerState.STOP:
            self.put_feedback("Processing cancelled.", LogType.DEBUG)

    def start(self):
        self.change_state(WorkerState.RUNNING)
        threading.Thread.start(self)

    def kill(self):
        self.change_state(WorkerState.STOP)
