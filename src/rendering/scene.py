# Copyright (C) 2018
# This notice is to be included in all relevant source files.
# "Brandon Goldbeck" <bpg@pdx.edu>
# “Anthony Namba” <anamba@pdx.edu>
# “Brandon Le” <lebran@pdx.edu>
# “Ann Peake” <peakean@pdx.edu>
# “Sohan Tamang” <sohan@pdx.edu>
# “An Huynh” <an35@pdx.edu>
# “Theron Anderson” <atheron@pdx.edu>
# This software is licensed under the MIT License.
# See LICENSE file for the full text.
import time
from src.rendering.basic_mesh_object import BasicMeshObject
from src.rendering.camera import Camera
from src.rendering.rendering_engine import RenderingEngine
from pyrr import *


class Scene:
    """The scene context that stores the references to models and sets up the camera to view the
    OpenGL 3D rendering environment.
    """
    _last_time = 0.0
    _ang_x = 0
    _ang_y = 0
    _camera_distance = 4.0
    _view = Vector3()

    def __init__(self):
        """Constructor to initialize the scene.
        """
        self.last_mouse_position = (0.0, 0.0)
        self.delta_mouse = (0.0, 0.0)
        self._last_time = time.process_time()
        self.active_scene_object = None
        self.mouse_rotate_sensitivity = 1.0
        self.scene_objects = {
            "camera": Camera("camera"),
            "input_model": None,
            "output_model": None
        }

        RenderingEngine.camera = self.scene_objects["camera"]
        RenderingEngine.camera.follow_distance = self._camera_distance
        RenderingEngine.camera.update()

    def on_mouse_move(self, event):
        """Called when the user moves the mouse.

        :param event: The wxpython Event.
        :return: None
        """
        point = event.GetPosition()
        if self.last_mouse_position == (0.0, 0.0):
            self.last_mouse_position = point

        if event.Dragging():
            self.delta_mouse = (
                point[0] - self.last_mouse_position[0],  # dx
                point[1] - self.last_mouse_position[1])  # dy

        self.last_mouse_position = point

    def on_mouse_wheel(self, event):
        """Called when the user uses the mouse wheel scroll.

        :param event: The wxpython Event.
        :return: None
        """
        self._camera_distance -= event.GetWheelRotation() / 500.0
        if self._camera_distance < 0.0:
            self._camera_distance = 0.0001

        RenderingEngine.camera.follow_distance = self._camera_distance
        RenderingEngine.camera.update()
        event.Skip()

    def draw(self):
        """Draw all the scene objects that are enabled.

        :return: None
        """
        for key, scene_object in self.scene_objects.items():
            if scene_object is not None:
                scene_object.draw()

    def update(self, dt: float):
        """Called by the OpenGLCanvas, which is called every loop by the GUIEventLoop.

         :param dt: The delta time between the last call.
         :return: None
         """
        # Move the camera based on mouse tracking.
        dy = self.delta_mouse[1] * self.mouse_rotate_sensitivity
        dx = self.delta_mouse[0] * self.mouse_rotate_sensitivity

        if self.active_scene_object is not None and (dx != 0 or dy != 0):
            # Rotation of the camera.
            self.active_scene_object.transform.euler_angles += Vector3([-dy, -dx, 0.0])
            RenderingEngine.camera.target = self.active_scene_object.transform.position

        RenderingEngine.camera.update()

        # Update the scene objects.
        for key, scene_object in self.scene_objects.items():
            if scene_object is not None:
                if scene_object.enabled:
                    scene_object.update()

        self.delta_mouse = (0.0, 0.0)

    def replace_input_model_mesh(self, mesh):
        """Replace the input model mesh with a new mesh.

        :param mesh: The new mesh.
        :return: None
        """
        self._replace_model_mesh("input_model", mesh)

    def replace_output_model_mesh(self, mesh):
        """Replace the output model mesh with a new mesh.

        :param mesh: The new mesh.
        :return: None
        """
        self._replace_model_mesh("output_model", mesh)

    def _replace_model_mesh(self, tag, mesh):
        """Replace the model mesh with a new mesh.

        :param mesh: The new mesh.
        :param tag: The tag to use to search for the scene object.
        :return: None
        """
        self.remove_scene_object(tag)
        if mesh is not None:
            self.scene_objects.update({tag: BasicMeshObject(tag, mesh)})
            self.scene_objects[tag].transform.position = Vector3([0.0, 0.0, 0.0])
            self.scene_objects[tag].transform.euler_angles = Vector3([0.0, 0.0, 0.0])
        else:
            self.scene_objects.update({tag: None})

    def set_input_model_active(self, value):
        """Set the input model active state.

        :param value: The enable/disable state of the model.
        :return: None
        """
        self._set_model_active("input_model", value)

    def set_output_model_active(self, value):
        """Set the output model active state.

        :param value: The enable/disable state of the model.
        :return: None
        """
        self._set_model_active("output_model", value)

    def _set_model_active(self, tag, value):
        """Set the model with tag active state.

        :param tag: The tag to use to search for the scene object.
        :param value: The enable/disable state of the model.
        :return: None
        """

        if self.scene_objects[tag] is not None:
            if value is True:
                self.active_scene_object = self.scene_objects[tag]
                self.scene_objects[tag].enable()
            else:
                self.scene_objects[tag].disable()

    def remove_scene_object(self, tag):
        """Destroy a scene object.

        :param tag: The tag to use to search for the scene object.
        :return: None
        """
        if self.scene_objects.get(tag) is not None:
            self.scene_objects.pop(tag)

    def get_main_camera(self):
        """Retrieve the main camera object.

        :return: The Camera object that is designated as the camera in the scene.
        """
        return self.scene_objects["camera"]

    def get_active_model(self):
        """Retrieve the current scene object model

        :return: The active model in the scene.
        """
        return self.active_scene_object

    def get_camera_distance_to_origin(self):
        """Retrieve the distance the main camera is from the origin.

        :return: The float distance the camera is from the origin.
        """
        return self._camera_distance

    def set_model_scale(self, scale: float):
        """Set the scale of the model's in the scene.

        :param scale: The new scale as float to use.
        :return: None
        """
        input_model = self.scene_objects["input_model"]
        output_model = self.scene_objects["output_model"]
        scale_vector = Vector3([scale, scale, scale])

        if input_model is not None:
            input_model.transform.scale = scale_vector
        if output_model is not None:
            output_model.transform.scale = scale_vector

    def set_mouse_rotation_sensitivity(self, value: float):
        """Set a new mouse rotation sensitivity.

        :param value: The new mouse rotation sensitivity.
        :return: None
        """
        self.mouse_rotate_sensitivity = value

    def get_mouse_rotation_sensitivity(self):
        """Retrieve the mouse sensitivity.

        :return: The current mouse rotation sensitivity.
        """
        return self.mouse_rotate_sensitivity
