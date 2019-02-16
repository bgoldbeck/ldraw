# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.

from src.threading.base_job import BaseJob
from src.log_messages.log_message import LogMessage
from src.log_messages.log_type import LogType
import time


class TestJobA(BaseJob):
    """This is a test job to show how a job should be written to work properly
    """
    def __init__(self, feedback_log):
        self.feedback_log = feedback_log
        super().__init__(feedback_log)

    def do_job(self):
        self.put_feedback(LogMessage(LogType.DEBUG, "Starting Test Job A"))

        for i in range(5, 0, -1):
            self.is_running.wait() # Blocks if running event is not set
            if self.is_killed: # Exit loop if job got kill signal
                break
            self.put_feedback(LogMessage(LogType.DEBUG,
                                         "Test Job A: Message #" + str(i)))

            time.sleep(0.5)

        self.is_running.wait()

        if not self.is_killed: # Job completed (not killed)
            self.put_feedback(LogMessage(LogType.DEBUG, "Finished Test Job A"))


        else: # Job was killed
            #do any cleanup before exiting
            self.put_feedback(LogMessage(LogType.DEBUG, "Cancelled during Test Job A"))


        self.is_done.set()  # Set this so thread manager knows job is done
