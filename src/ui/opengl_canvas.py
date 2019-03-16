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
from wx import glcanvas
from src.rendering.scene import Scene
from OpenGL.GL import *
from src.ui.application_state import ApplicationState
from src.ui.user_event import UserEvent
from src.ui.user_event_type import UserEventType
from src.ui.iui_behavior import IUIBehavior
from src.model_conversion.model_shipper import ModelShipper
from src.ui.ui_driver import UIDriver
from src.log_messages.float_message import FloatMessage
from src.log_messages.log_type import LogType
from src.ui.ui_style import UIStyle
from src.rendering.rendering_engine import RenderingEngine
from pyrr import Vector3


class OpenGLCanvas(glcanvas.GLCanvas, IUIBehavior):
    """This is the canvas for OpenGL to render objects to.
    """
    canvas_size = (400, 300)

    def __init__(self, parent):
        """Default constructor for OpenGLCanvas class.

        :param parent: The parent wx control object.
        """
        # Call the base constructor for the OpenGL canvas.
        glcanvas.GLCanvas.__init__(self, parent, -1, size=self.canvas_size)
        self.parent = parent
        self.scene = None
        self.context = None
        self.scene = None
        self.wire_frame = False
        self.interacted = False
        self.canvas_color = Vector3([0.0, 0.0, 0.3])
        self.init = False
        self.aspect_ratio = self.canvas_size[0] / self.canvas_size[1]
        self.is_painting = True

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)
        self.Bind(wx.EVT_MOTION, self.on_mouse_move)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.process_erase_background)

        if not self.init:
            self.init_gl()
            self.init = True

    def on_mouse_move(self, event):
        """Called when the user moves the mouse.

        :param event: The wxpython Event.
        :return: None
        """
        if ModelShipper.input_model is not None:
            self.scene.on_mouse_move(event)

    def on_mouse_wheel(self, event):
        """Called when the user scrolls with the mouse wheel. We will notify all panels of the
        mouse wheel instance.

        :param event: The wxpython Event.
        :return: None
        """
        if ModelShipper.input_model is not None:
            self.scene.on_mouse_wheel(event)
            UIDriver.fire_event(UserEvent(
                UserEventType.RENDERING_MOUSE_WHEEL_EVENT,
                FloatMessage(
                    LogType.IGNORE,
                    "Mouse Moved",
                    self.scene.get_camera_distance_to_origin())))

    def on_paint(self, event):
        """Event that occurs when the canvas paint event is called.

        :param event: The wxpython Event.
        :return: None
        """
        wx.PaintDC(self)
        if self.init:
            self.draw()

    def init_gl(self):
        """Initialize OpenGL functionality.

        :return: None
        """
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)
        if glInitGl42VERSION():
            glClearColor(UIStyle.opengl_canvas_background_color[0],  # Red
                         UIStyle.opengl_canvas_background_color[1],  # Green
                         UIStyle.opengl_canvas_background_color[2],  # Blue
                         UIStyle.opengl_canvas_background_color[3])  # Alpha

            glEnable(GL_DEPTH_TEST)

            glViewport(0, 0, self.canvas_size[0], self.canvas_size[1])
            self.scene = Scene()
            self.Show()

        print("OpenGL Major: " + str(RenderingEngine.gl_version_major_minor()[0]))
        print("OpenGL Minor: " + str(RenderingEngine.gl_version_major_minor()[1]))
        print("GLSL Major: " + str(RenderingEngine.glsl_version_major_minor()[0]))
        print("GLSL Minor: " + str(RenderingEngine.glsl_version_major_minor()[1]))

    def draw(self):
        """Draw the previous OpenGL buffer with all the 3D data.
        :return: None
        """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.wire_frame is True:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        self.Refresh()
        if self.scene is not None:
            self.scene.draw()
        self.SwapBuffers()

    def on_state_changed(self, new_state: ApplicationState):
        """A state change was passed to the OpenGLCanvas.

        :param new_state: The recorded ApplicationState.
        :return: None
        """
        pass

    def on_event(self, event: UserEvent):
        """A user event was passed to the OpenGLCanvas.

        :param event: The recorded UserEvent.
        :return: None
        """
        if glInitGl42VERSION():
            if event is not None:
                if event.get_event_type() == UserEventType.INPUT_MODEL_READY:
                    self.scene.replace_input_model_mesh(ModelShipper.input_model.mesh)
                    self.scene.replace_output_model_mesh(None)
                    self.scene.set_input_model_active(True)
                    
                if event.get_event_type() == UserEventType.RENDERING_WIRE_FRAME_PRESSED:
                    # A log message of this type is a BoolMessage.
                    self.wire_frame = event.get_log_message().get_bool()
                    
                if event.get_event_type() == UserEventType.RENDERING_CANVAS_DISABLE:
                    self.Unbind(wx.EVT_PAINT)
                    self.Unbind(wx.EVT_PAINT)
                    self.Refresh()
                    
                if event.get_event_type() == UserEventType.RENDERING_CANVAS_ENABLE:
                    self.Bind(wx.EVT_PAINT, self.on_paint)
                    self.Refresh()

    def update(self, dt: float):
        """Called every loop by the GUIEventLoop

        :param dt: The delta time between the last call.
        :return: None
        """
        if self.scene is not None:
            self.scene.update(dt)

    def process_erase_background(self, event):
        """Process the erase background event.
        """
        pass  # Do nothing, to avoid flashing on MSWin

    def update_meshes(self):
        """Update the meshes in the scene with the Modelshipper models, if they exist.

        :return: None
        """
        if ModelShipper.output_model is not None:
            print("Update output model")
            self.scene.replace_output_model_mesh(ModelShipper.output_model.get_mesh())
        if ModelShipper.input_model is not None:
            print("Update input model")
            self.scene.replace_input_model_mesh(ModelShipper.input_model.mesh)

    def set_output_preview_active(self):
        """Set the state of the output model to active.

        :return: None.
        """
        self.scene.set_output_model_active(True)

    def set_input_preview_active(self):
        """Set the state of the input model to active.

        :return: None.
        """
        self.scene.set_input_model_active(True)

    def set_output_preview_inactive(self):
        """Set the state of the output model to inactive.

        :return: None.
        """
        self.scene.set_output_model_active(False)

    def set_input_preview_inactive(self):
        """Set the state of the input model to inactive.

        :return: None.
        """
        self.scene.set_input_model_active(False)
