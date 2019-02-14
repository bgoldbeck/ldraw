# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.

from src.log_messages.log_message import LogMessage
from src.log_messages.output_model_message import OutputModelMessage
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

    def put_feedback(self, msg, log_type):
        """Puts a LogMessage into the feedback queue
        :param msg: message text
        :param log_type: type of log
        :return: None
        """
        log_msg = LogMessage(log_type, msg)
        self.feedback_log.put(log_msg)

    def put_model_out(self, log_type, msg, model):
        """Puts a LogMessage into the feedback queue
        :param msg: message text
        :param log_type: type of log
        :param model: ldraw model
        :return: None
        """
        out_msg = OutputModelMessage(log_type, msg, model)
        self.feedback_log.put(out_msg)
