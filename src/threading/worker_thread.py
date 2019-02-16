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
    """Thread for handling algorithms/processing stuff
    """
    def __init__(self, feedback_log, job_list):
        threading.Thread.__init__(self)
        self.feedback_log = feedback_log
        self.job_list = []
        for job in job_list: #fill up job list with new instances
            self.job_list.append(job(feedback_log))
        self.current_job = None
        self.state = WorkerState.RUNNING

    def run(self):
        """Process the thread and do work with its CPU time.

        :return: None
        """
        for job in self.job_list:
            if self.state == WorkerState.STOP:
                break # Stop doing jobs if killed
            # add a check for if paused here too... maybe use an event
            self.current_job = job
            if(self.current_job and not self.current_job.is_running.isSet()):
                self.current_job.go()

            self.current_job.do_job()
            self.current_job.is_done.wait()

        if self.state != WorkerState.STOP:
            self.put_feedback("All jobs complete", LogType.DEBUG)

    def put_feedback(self, msg, log_type):
        """Puts a LogMessage into the feedback queue
        :param msg: message text
        :param log_type: type of log
        :return: None
        """
        log_msg = LogMessage(log_type, msg)
        self.feedback_log.put(log_msg)

    def change_state(self, new_state):
        """Changes worker thread state (run/pause/stop)

        :param new_state: WorkerState to set the worker to
        :return:
        """
        self.state = new_state
        if new_state == WorkerState.RUNNING:
            if self.current_job:
                self.current_job.go()
            self.put_feedback("Beginning processing.", LogType.DEBUG)
        elif new_state == WorkerState.PAUSE:
            self.current_job.pause()
            self.put_feedback("Processing paused.", LogType.DEBUG)
        elif new_state == WorkerState.STOP:
            self.current_job.is_killed = True
            self.current_job.go()
            self.put_feedback("Processing cancelled.", LogType.DEBUG)


    def start(self):
        """Change worker state to RUNNING and start its main routine

        :return: None
        """
        self.change_state(WorkerState.RUNNING)
        threading.Thread.start(self)

    def kill(self):
        """Change worker state to STOP

        :return: None
        """
        self.change_state(WorkerState.STOP)

