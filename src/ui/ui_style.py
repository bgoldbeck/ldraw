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


class UIStyle:
    """The UI style class holds all information about size, background color,
    border and text color.
    The color scheme in this class is the default color (for debug).
    """
    # Utility
    button_background = ""
    button_text = ""

    # Main Frame
    main_frame_border = wx.DEFAULT_DIALOG_STYLE
    main_frame_size = (1024, 640)

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

    # OpenGL
    opengl_panel_border = wx.BORDER_SUNKEN
    opengl_panel_size = (1024, 300)
    opengl_canvas_background_color = [0, 0, 0, 255]
    opengl_label_color = "#666666"
    opengl_input_background = "#ffffff"
    opengl_input_foreground = "#111111"

    @staticmethod
    def setup_dark_theme():
        """Set up dark color theme for program.
        """
        # Utility
        # UIStyle.button_background = "#2B2B2B"
        # UIStyle.button_text = "#A9B7C6"

        # Main Frame
        UIStyle.main_frame_border = wx.DEFAULT_FRAME_STYLE
        UIStyle.main_frame_min_size = (1024, 640)
        UIStyle.main_frame_max_size = (1024, 900)
        UIStyle.main_frame_current_size = UIStyle.main_frame_min_size

        # Main Panel
        UIStyle.main_panel_background_color = "#2B2B2B"

        # Metadata Panel
        UIStyle.metadata_border = wx.BORDER_SUNKEN
        UIStyle.metadata_background_color = "#2B2B2B"
        UIStyle.metadata_label_color = "#808080"
        UIStyle.metadata_input_text_color = "#A5C25C"
        UIStyle.metadata_input_valid_background = "#323232"
        UIStyle.metadata_input_invalid_background = "#D25252"

        UIStyle.metadata_text_ctrl_size = (400, 20)
        UIStyle.metadata_big_button = (120, 25)
        UIStyle.metadata_small_button_size = (30, 25)
        UIStyle.metadata_panel_size = (1024, 100)
        UIStyle.metadata_label_size = (200, 25)

        # Conversion Panel
        UIStyle.conversion_border = wx.SIMPLE_BORDER
        UIStyle.conversion_background_color = "#2B2B2B"
        UIStyle.conversion_big_button_size = (120, 30)

        # Log Panel
        UIStyle.log_border = wx.BORDER_SUNKEN
        UIStyle.log_background_color = "#2B2B2B"
        UIStyle.log_text_background_color = "#323232"
        UIStyle.log_default_text_color = "#A9B7C6"
        UIStyle.log_info_text_color = "white"
        UIStyle.log_warning_text_color = "#FFC66D"
        UIStyle.log_debug_text_color = "#BED6FF"
        UIStyle.log_error_text_color = "#D25252"

        UIStyle.log_big_button = (70, 25)
        UIStyle.log_output_size = (920, 165)
        UIStyle.log_panel_size = (1022, 500)
        UIStyle.log_font_size = 10

        # OpenGL Panel
