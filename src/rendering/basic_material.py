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
from OpenGL.GL import *
import OpenGL.GL.shaders
from pyrr import *
from src.rendering.rendering_engine import RenderingEngine
from src.rendering.material import Material
from PIL import Image
import numpy
from src.util import Util


class BasicMaterial(Material):
    """This class controls the shader material information and determines how the mesh object should look
    in the OpenGL rendering context.
    """

    def __init__(self, triangle_data):
        """Constructor for the BasicMaterial.

        :param triangle_data: The triangle data to use in OpenGL Rendering context.
        """
        Material.__init__(self)

        self.vertex_shader = """
# version 420
in layout(location = 0) vec3 vertex_position;
in layout(location = 1) vec2 vertex_uv;
in layout(location = 2) vec3 vertex_normal;

out vec2 uv;
out vec3 position_worldspace;
out vec3 normal_cameraspace;
out vec3 eye_direction_cameraspace;
out vec3 light_direction_cameraspace;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform vec3 light_position_worldspace;

void main() {
    // Output position of the vertex, in clip space
    gl_Position = projection * view * model *  vec4(vertex_position, 1.0);

    // Position of the vertex, in worldspace : M * position
    position_worldspace = (model * vec4(vertex_position,1)).xyz;


    // Vector that goes from the vertex to the camera, in camera space.
    // In camera space, the camera is at the origin (0,0,0).
    vec3 vertex_position_cameraspace = (view * model * vec4(vertex_position,1)).xyz;
    eye_direction_cameraspace = vec3(0,0,0) - vertex_position_cameraspace;

    // Vector that goes from the vertex to the light, in camera space. M is ommited because it's identity.
    vec3 light_position_cameraspace = (view * vec4(light_position_worldspace,1)).xyz;
    light_direction_cameraspace = light_position_cameraspace + eye_direction_cameraspace;

    // Normal of the the vertex, in camera space
    // Only correct if ModelMatrix does not scale the model ! Use its inverse transpose if not.
    normal_cameraspace = (view * model * vec4(vertex_normal,0)).xyz; 

    // UV of the vertex. No special space for this one.
    uv = vertex_uv;
}
"""

        self.fragment_shader = """
# version 420

// Interpolated values from the vertex shaders
in vec2 uv;
in vec3 position_worldspace;
in vec3 normal_cameraspace;
in vec3 eye_direction_cameraspace;
in vec3 light_direction_cameraspace;

// Ouput data
out vec3 color;


uniform sampler2D texture_sampler;
uniform vec3 light_position_worldspace = vec3(0,0,0);

// Light emission properties
uniform vec3 light_color = vec3(0,1,0);
uniform float light_power = 50.0f;
uniform vec3 ambient_color = vec3(0.3, 0.3, 0.3);
uniform vec3 specular_color = vec3(0.2, 0.2, 0.2);

void main() {
    // Material properties
    vec3 material_diffuse_color = texture(texture_sampler, uv ).rgb;
    vec3 material_ambient_color = ambient_color * material_diffuse_color;

    // Distance to the light
    float distance = length(light_position_worldspace - position_worldspace );

    // Normal of the computed fragment, in camera space
    vec3 n = normalize(normal_cameraspace );

    // Direction of the light (from the fragment to the light)
    vec3 l = normalize(light_direction_cameraspace );

    // Cosine of the angle between the normal and the light direction, 
    // clamped above 0
    //  - light is at the vertical of the triangle -> 1
    //  - light is perpendicular to the triangle -> 0
    //  - light is behind the triangle -> 0
    float cos_theta = clamp( dot( n,l ), 0,1 );

    // Eye vector (towards the camera)
    vec3 eye_vector = normalize(eye_direction_cameraspace);
    // Direction in which the triangle reflects the light
    vec3 reflection = reflect(-l,n);
    // Cosine of the angle between the Eye vector and the Reflect vector,
    // clamped to 0
    //  - Looking into the reflection -> 1
    //  - Looking elsewhere -> < 1
    float cos_alpha = clamp(dot(eye_vector, reflection), 0,1 );

    color = 
        // Ambiant : simulates indirect lighting
        material_ambient_color +
        // Diffuse : "color" of the object
        material_diffuse_color * light_color * light_power * cos_theta / (distance*distance) +
        // Specular : reflective highlight, like a mirror
        specular_color * light_color * light_power * pow(cos_alpha,5) / (distance*distance);
}
"""

        self.shader = OpenGL.GL.shaders.compileProgram(
            OpenGL.GL.shaders.compileShader(self.vertex_shader,
                                            GL_VERTEX_SHADER),
            OpenGL.GL.shaders.compileShader(self.fragment_shader,
                                            GL_FRAGMENT_SHADER))

        glUseProgram(self.shader)

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, len(triangle_data) * 4, triangle_data, GL_STATIC_DRAW)

        # Positions input to shader.
        glVertexAttribPointer(0,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              32,
                              ctypes.c_void_p(0))

        # UV input to shader
        glVertexAttribPointer(1,
                              2,
                              GL_FLOAT,
                              GL_FALSE,
                              32,
                              ctypes.c_void_p(12))

        # Normal input to shader
        glVertexAttribPointer(2,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              32,
                              ctypes.c_void_p(20))

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)
        texture = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texture)
        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # load image
        image = Image.open(Util.path_conversion("assets/images/default_brick_diffuse.jpg"))
        img_data = numpy.array(list(image.getdata()), numpy.uint8)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glEnable(GL_TEXTURE_2D)

        self.set_uniform_matrix4fv("view",
                                   RenderingEngine.camera.get_view_matrix())

        self.set_uniform_matrix4fv("projection",
                                   RenderingEngine.projection)

        self.set_uniform3f("light_position_worldspace", Vector3([0.0, 10.0, 10.0]))
        self.set_uniform3f("light_color", Vector3([0.0, 0.0, 1.0]))
        self.set_uniform3f("ambient_color", Vector3([0.5, 0.5, 0.5]))
        self.set_uniform3f("specular_color", Vector3([0.3, 0.3, 0.3]))
        self.set_uniform3f("light_color", Vector3([0.2, 0.2, 0.2]))
        self.set_uniform1f("light_power", 100.0)

    def set_view_matrix(self, view_matrix):
        """Update the view matrix.

        :param view_matrix: The new view Matrix44.
        :return: None
        """
        self.set_uniform_matrix4fv("view", view_matrix)

    def set_model_matrix(self, model_matrix):
        """Update the model matrix.

        :param model_matrix: The new model Matrix44.
        :return: None
        """
        self.set_uniform_matrix4fv("model", model_matrix)
