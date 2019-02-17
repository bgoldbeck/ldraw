# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
from enum import Enum


class UserEventType(Enum):
    """The enumerated class the stores the possible user event types.
    """
    INPUT_MODEL_READY = 0
    SELECTED_OUTPUT_FILE = 1
    CONVERSION_COMPLETE = 2
    CONVERSION_FAILED = 3
    CONVERSION_CANCELED = 4
    CONVERSION_PAUSED = 5
    CONVERSION_STARTED = 6
    WORKER_LOG_MESSAGE_AVAILABLE = 7
    INPUT_VALIDATION = 8
    APPLICATION_STATE_CHANGE = 9
    RENDERING_WIRE_FRAME_PRESSED = 10
    RENDERING_MOUSE_WHEEL_EVENT = 11
    RENDERING_SELECT_STL_PREVIEW = 12
    RENDERING_SELECT_LDRAW_PREVIEW = 13
    RENDERING_CANVAS_ENABLE = 14
    RENDERING_CANVAS_DISABLE = 15
