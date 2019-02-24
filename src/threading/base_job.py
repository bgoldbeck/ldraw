# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.

import threading

class BaseJob:
    """The pseudo interface for processing jobs to
    inherit method properties from.
    """

    def __init__(self, feedback_log):
        """Initialize class members

        """
        self.feedback_log = feedback_log
        self.is_done = threading.Event()
        self.is_running = threading.Event()
        self.is_killed = False
        self.status = ""
        self.name = ""


    def do_job(self):
        """The main work of the job. (Essentially a virtual class here)
        :return:
        """
        pass

    def get_work(self):
        """Gets the results of the job,
        :return:
        """
        pass

    def pause(self):
        """Clear running event

        :return: None
        """
        self.is_running.clear()

    def go(self):
        """Set running event

        :return: None
        """
        self.is_running.set()

    def put_feedback(self, log_msg):
        """Puts a LogMessage into the feedback queue
        :param msg: message text
        :param log_type: type of log
        :return: None
        """
        self.feedback_log.put(log_msg)

    def get_status(self):
        """Gets status of job as string
        :return: None
        """
        return self.status

