
import math
from pathlib import Path

import numpy as np

from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    glClear,
    glClearColor,
    glEnable,
    glViewport,
)

from framework.core.base import Base
from framework.core.shader_program import ShaderProgram
from framework.core_ext.camera import Camera
from framework.core_ext.mesh import Mesh
from framework.geometry.box import create_box_geometry


class BesouroCaracolApp(Base):
    """Aplicacao principal de Computacao Grafica."""

    def initialize(self):
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, 960, 540)
        glClearColor(0.08, 0.10, 0.16, 1.0)

        root = Path(__file__).resolve().parent

        self.shader = ShaderProgram(
            root / "shaders" / "basic.vert",
            root / "shaders" / "basic.frag",
        )

        self.camera = Camera(
            position=(0, 1.5, 5),
            target=(0, 0, 0),
            aspect_ratio=960 / 540,
        )

        self.cube = Mesh(create_box_geometry())

        print("Cena tridimensional inicializada com sucesso!")

    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Rotacao controlada pelo tempo decorrido.
        angle = self.time * 0.8

        c = math.cos(angle)
        s = math.sin(angle)

        model = np.array(
            [
                [c, 0, s, 0],
                [0, 1, 0, 0],
                [-s, 0, c, 0],
                [0, 0, 0, 1],
            ],
            dtype=np.float32,
        )

        self.shader.use()

        self.shader.set_matrix4("uModel", model)
        self.shader.set_matrix4(
            "uView", self.camera.get_view_matrix()
        )
        self.shader.set_matrix4(
            "uProjection",
            self.camera.get_projection_matrix(),
        )

        self.cube.draw()


if __name__ == "__main__":
    app = BesouroCaracolApp()
    app.run()
