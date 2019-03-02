# Copyright (C) 2018 - This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License. See LICENSE file for the full text.
import wx, time
from wx.lib.masked import NumCtrl
from OpenGL.GL import *
from src.ui.opengl_canvas import OpenGLCanvas
from src.ui.iui_behavior import IUIBehavior
from src.ui.application_state import ApplicationState
from src.ui.user_event import UserEvent
from src.ui.user_event_type import UserEventType
from src.ui.ui_driver import UIDriver
from src.log_messages.log_message import LogMessage
from src.log_messages.float_message import FloatMessage
from src.log_messages.bool_message import BoolMessage
from src.log_messages.log_type import LogType
from src.ui.ui_style import *
from src.ui.button import Button


class OpenGLPanel(wx.Panel, IUIBehavior):
    """Holds wx controls relevant to controlling the program behavior for starting, stopping,
    pausing, and canceling the conversion process.
    """

    def __init__(self, parent):
        """Default constructor for ConversionPanel class.

        :param parent: The parent wx object for this panel.
        """
        wx.Panel.__init__(self, parent, size=UIStyle.opengl_panel_size, style=UIStyle.conversion_border)
        self.parent = parent
        self.stl_preview_context = True
        self.cb_wire_frame = None
        self.zoom_static_text_ctrl = None
        self.scale_static_text = None
        self.scale_up_button = None
        self.scale_down_button = None
        self.scale_input = None
        self.cycle_preview_button = None
        self.camera_rotation_static_text_ctrl = None
        self.camera_position_static_text_ctrl = None
        self.help_rotate_static_text_ctrl = None
        self.help_zoom_static_text_ctrl = None
        self.opengl_canvas = None
        self.timer = 0
        self._build_gui()

    def _build_gui(self):
        """Initializing wx objects that make up this OpenGL panel and their layout within.

        :return: None
        """
        # Create the controls.
        self.cb_wire_frame = wx.CheckBox(self, label=" Wireframe")
        self.cb_wire_frame.SetForegroundColour(UIStyle.opengl_label_color)

        self.zoom_static_text_ctrl = wx.StaticText(self, size=(150, 30))
        self.zoom_static_text_ctrl.SetLabelText("Camera Distance to Origin: ")
        self.zoom_static_text_ctrl.SetForegroundColour(UIStyle.opengl_label_color)

        self.scale_static_text = wx.StaticText(self, label="Scale:", size=(50, 20))
        self.scale_static_text.SetForegroundColour(UIStyle.metadata_label_color)

        self.scale_up_button = Button(self, label="+", size=(23, 23))

        self.scale_down_button = Button(self, label="-", size=(23, 23))

        self.scale_input = wx.lib.masked.NumCtrl(
            self,
            value=1.0,
            size=(100, 20),
            integerWidth=10,
            fractionWidth=10,
            min=0.0)
        self.scale_input.SetBackgroundColour(UIStyle.opengl_input_background)
        self.scale_input.SetForegroundColour(UIStyle.opengl_input_foreground)

        self.cycle_preview_button = Button(self, label="Preview LDraw Model", size=(150, 30))
        self.cycle_preview_button.Disable()

        self.camera_rotation_static_text_ctrl = wx.StaticText(self, size=(270, 20))
        self.camera_rotation_static_text_ctrl.SetLabelText("Model Rotation: ")
        self.camera_rotation_static_text_ctrl.SetForegroundColour(UIStyle.opengl_label_color)

        self.camera_position_static_text_ctrl = wx.StaticText(self, size=(270, 20))
        self.camera_position_static_text_ctrl.SetLabelText("Camera Position: ")
        self.camera_position_static_text_ctrl.SetForegroundColour(UIStyle.opengl_label_color)

        self.help_rotate_static_text_ctrl = wx.StaticText(self, size=(270, 50))
        self.help_rotate_static_text_ctrl.SetLabelText("Hold left click while moving the mouse to rotate the camera.")
        self.help_rotate_static_text_ctrl.SetForegroundColour(UIStyle.opengl_label_color)
        self.help_rotate_static_text_ctrl.SetFont(wx.Font(12, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))

        self.help_zoom_static_text_ctrl = wx.StaticText(self, size=(270, 50))
        self.help_zoom_static_text_ctrl.SetLabelText("Use the mouse wheel to zoom the camera from the origin.")
        self.help_zoom_static_text_ctrl.SetForegroundColour(UIStyle.opengl_label_color)
        self.help_zoom_static_text_ctrl.SetFont(wx.Font(12, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))

        self.preview_render_context = wx.StaticText(self, size=(270, 20))
        self.preview_render_context.SetLabelText("Current Preview: ")
        self.preview_render_context.SetForegroundColour(UIStyle.opengl_label_color)

        self.opengl_canvas = OpenGLCanvas(self)
        show = glInitGl42VERSION()
        # Build the layout and show the controls if correct OpenGL version
        self._build_layout(show)

        # Bind events to functions.
        self.Bind(wx.EVT_CHECKBOX, self.on_wire_frame_pressed, self.cb_wire_frame)
        self.Bind(wx.EVT_BUTTON, self.on_cycle_preview_pressed, self.cycle_preview_button)
        self.Bind(wx.EVT_BUTTON, self.on_scale_up, self.scale_up_button)
        self.Bind(wx.EVT_BUTTON, self.on_scale_down, self.scale_down_button)

        self.scale_input.Bind(wx.lib.masked.EVT_NUM, self.on_scale_value_changed)

        # Disable widgets until they are necessary from application state context.
        self.set_widget_rendering_contexts(False)

    def _build_layout(self, show: bool):
        """Set up how the wx controls are laid out on the log panel.

        :param show: Whether or not to enable all the controls of this panel.
        :return:
        """
        self.cb_wire_frame.Show(show)
        self.zoom_static_text_ctrl.Show(show)
        self.scale_static_text.Show(show)
        self.scale_up_button.Show(show)
        self.scale_down_button.Show(show)
        self.scale_input.Show(show)
        self.cycle_preview_button.Show(show)
        self.camera_rotation_static_text_ctrl.Show(show)
        self.camera_position_static_text_ctrl.Show(show)
        self.help_rotate_static_text_ctrl.Show(show)
        self.help_zoom_static_text_ctrl.Show(show)
        self.opengl_canvas.Show(show)

        # Layout the UI
        # Left Side
        left_vertical_layout = wx.BoxSizer(wx.VERTICAL)
        left_vertical_layout.AddSpacer(10)
        left_vertical_layout.Add(self.cb_wire_frame, 0, wx.ALIGN_LEFT)
        left_vertical_layout.AddSpacer(10)
        left_vertical_layout.Add(self.scale_static_text, 0, wx.ALIGN_LEFT)

        scale_horizontal_layout = wx.BoxSizer(wx.HORIZONTAL)
        scale_horizontal_layout.Add(self.scale_down_button, 0, wx.ALIGN_LEFT)
        scale_horizontal_layout.Add(self.scale_input, 0, wx.ALIGN_LEFT)
        scale_horizontal_layout.Add(self.scale_up_button, 0, wx.ALIGN_LEFT)
        scale_horizontal_layout.AddSpacer(115)

        left_vertical_layout.Add(scale_horizontal_layout)
        left_vertical_layout.AddSpacer(10)
        left_vertical_layout.Add(self.cycle_preview_button)
        left_vertical_layout.AddSpacer(10)
        left_vertical_layout.Add(self.preview_render_context)

        horizontal_layout = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_layout.Add(left_vertical_layout)

        # Middle
        horizontal_layout.Add(self.opengl_canvas, 0, wx.ALIGN_LEFT)

        # Right Side
        right_vertical_layout = wx.BoxSizer(wx.VERTICAL)
        right_vertical_layout.AddSpacer(10)
        right_vertical_layout.Add(self.camera_rotation_static_text_ctrl, wx.ALIGN_LEFT)
        right_vertical_layout.Add(self.camera_position_static_text_ctrl, wx.ALIGN_LEFT)
        right_vertical_layout.Add(self.zoom_static_text_ctrl, wx.ALIGN_LEFT)
        right_vertical_layout.AddSpacer(40)
        right_vertical_layout.Add(self.help_rotate_static_text_ctrl, wx.ALIGN_RIGHT)
        right_vertical_layout.AddSpacer(10)
        right_vertical_layout.Add(self.help_zoom_static_text_ctrl, wx.ALIGN_RIGHT)

        horizontal_layout.AddSpacer(5)
        horizontal_layout.Add(right_vertical_layout, 0, wx.ALIGN_RIGHT)

        self.SetSizer(horizontal_layout)

    def on_state_changed(self, new_state: ApplicationState):
        """A state change was passed to the ConversionPanel.

        :param new_state: The recorded ApplicationState.
        :return: None
        """
        pass

    def on_event(self, event: UserEvent):
        """A user event was passed to the ConversionPanel.

        :param event: The recorded UserEvent.
        :return: None
        """
        if not glInitGl42VERSION():
            return

        if event is not None:
            if event.get_event_type() == UserEventType.CONVERSION_COMPLETE:
                self.opengl_canvas.update_meshes()
                self.cycle_preview_button.Enable()
                self.set_preview_from_context()

            if event.get_event_type() == UserEventType.RENDERING_MOUSE_WHEEL_EVENT:
                if self.can_use_opengl():
                    # Log Message here is of derived class FloatMessage.
                    if isinstance(event.get_log_message(), FloatMessage):
                        self.zoom_static_text_ctrl.SetLabelText(
                            "Camera Distance to Origin: {0:0.3f}".format(event.get_log_message().get_float()))
            elif event.get_event_type() == UserEventType.INPUT_MODEL_READY:
                if self.can_use_opengl():
                    self.preview_render_context.SetLabelText("Current Preview: STL Model")
                    self.set_widget_rendering_contexts(True)
                    self.cycle_preview_button.Disable()
                    self.zoom_static_text_ctrl.SetLabelText(
                        "Camera Distance to Origin: " + str(self.opengl_canvas.scene.get_camera_distance_to_origin()))

    def on_wire_frame_pressed(self, event):
        """Send an event that the wire frame button was pressed. The OpenGLCanvas will
        detect and react accordingly.

        :param event: The wxpython event that occured.
        :return: None
        """
        UIDriver.fire_event(UserEvent(
            UserEventType.RENDERING_WIRE_FRAME_PRESSED,
            BoolMessage(
                LogType.DEBUG, "Wire frame checkbox pressed.",
                self.cb_wire_frame.GetValue())
        ))
        event.Skip()

    def on_cycle_preview_pressed(self, event):
        """The user pressed the cycle preview button to switch between previewing stl and ldraw model.

        :param event: The wxpython Event.
        :return: None
        """
        self.stl_preview_context = not self.stl_preview_context
        self.set_preview_from_context()
        event.Skip()

    def set_preview_from_context(self):
        """Update the preview label and models based on our current contextual state.

        :return: None
        """
        if self.stl_preview_context is True:
            self.cycle_preview_button.SetLabelText("Preview LDraw Model")
            self.opengl_canvas.set_output_preview_inactive()
            self.opengl_canvas.set_input_preview_active()
            self.preview_render_context.SetLabelText("Current Preview: STL Model")
        else:
            self.cycle_preview_button.SetLabelText("Preview STL Model")
            self.opengl_canvas.set_input_preview_inactive()
            self.opengl_canvas.set_output_preview_active()
            self.preview_render_context.SetLabelText("Current Preview: LDraw Model")

    def on_scale_value_changed(self, event):
        """The scale input value has been modified by the user. Notify the OpenGL scene
        of the new scale value.

        :param event: The wxpython Event.
        :return: None
        """
        self.update_model_scale()
        event.Skip()

    def update_model_scale(self):
        """Update the model scale to reflect the value within the scale input control.

        :return: None
        """
        self.opengl_canvas.scene.set_model_scale(self.scale_input.GetValue())

    def set_widget_rendering_contexts(self, enabled):
        """Disable or enable the controls the user may press on the OpenGL Panel.

        :param enabled: Whether to enable or disable the controls.
        :return: None
        """
        self.scale_down_button.Enabled = enabled
        self.cb_wire_frame.Enabled = enabled
        self.scale_input.Enabled = enabled
        self.cycle_preview_button.Enabled = enabled
        self.scale_up_button.Enabled = enabled

    def on_scale_up(self, event):
        """User pressed the scale up button.

        :param event: The wxpython Event.
        :return: None
        """
        value = self.scale_input.GetValue()
        self.scale_input.SetValue(value + 0.125)
        event.Skip()

    def on_scale_down(self, event):
        """User pressed the scale down button.

        :param event: The wxpython Event.
        :return: None
        """
        value = self.scale_input.GetValue()
        self.scale_input.SetValue(value - 0.125)
        event.Skip()

    def update(self, dt: float):
        """Called every loop by the GUIEventLoop

        :param dt: The delta time between that last call.
        :return: None
        """
        self.timer += dt
        delay = 0.20  # Activate timer every 200 ms
        if self.timer > delay:
            self.timer = 0
            if self.opengl_canvas is not None:
                scene = self.opengl_canvas.scene
                if scene is not None:
                    camera = scene.get_main_camera()
                    active_model = scene.get_active_model()
                    if camera is not None and active_model is not None:
                        rotation = active_model.transform.euler_angles
                        position = camera.transform.position
                        # Update the camera rotation and position metrics on screen.
                        self.camera_rotation_static_text_ctrl.SetLabelText(
                            "Model Rotation: [{0:0.3f}, {1:0.3f}, {2:0.3f}]".format(
                                rotation[0],
                                rotation[1],
                                rotation[2]))
                        self.camera_position_static_text_ctrl.SetLabelText(
                            "Camera Position: [{0:0.3f}, {1:0.3f}, {2:0.3f}]".format(
                                position[0],
                                position[1],
                                position[2]))

    def can_use_opengl(self):
        return self.opengl_canvas is not None and glInitGl42VERSION()

