# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import wx


class UI_style():
    """The UI style class holds all information about size, background color,
    border and text color.
    The color scheme in this class is the default color (for debug).
    """
    # Utility
    button_background = ""
    button_text = ""

    # Main Frame
    main_frame_border = wx.DEFAULT_FRAME_STYLE
    main_frame_min_size = (1024, 640)
    main_frame_max_size = (1024, 900)
    main_frame_current_size = main_frame_min_size

    # Main Panel
    main_panel_background_color = "#ffffaa"

    # Metadata Panel
    metadata_border = wx.BORDER_SUNKEN
    metadata_background_color = "#777fea"
    metadata_label_color = ""
    metadata_input_text_color = "black"
    metadata_input_valid_background = ""
    metadata_input_invalid_background = "pink"

    metadata_text_ctrl_size = (400, 20)
    metadata_big_button = (120, 25)
    metadata_small_button_size = (30, 25)
    metadata_panel_size = (1024, 100)
    metadata_label_size = (200, 25)

    # Conversion Panel
    conversion_border = wx.SIMPLE_BORDER
    conversion_background_color = "#456eab"
    conversion_big_button_size = (120, 30)

    # Log Panel
    log_border = wx.BORDER_SUNKEN
    log_background_color = "#eee111"
    log_text_background_color = [25, 25, 25]
    log_default_text_color = [225, 225, 225]
    log_info_text_color = [225, 225, 225]
    log_warning_text_color = [255, 255, 0]
    log_debug_text_color = [0, 150, 250]
    log_error_text_color = [255, 0, 0]

    log_big_button = (70, 25)
    log_output_size = (920, 165)
    log_panel_size = (1022, 500)
    log_font_size = 9
