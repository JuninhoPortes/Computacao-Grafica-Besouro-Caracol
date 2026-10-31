
import math
from pathlib import Path

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
from framework.core_ext.object3d import Object3D
from framework.geometry.box import create_box_geometry


class BesouroCaracolApp(Base):
    """Aplicacao principal de Computacao Grafica."""

    def initialize(self):
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, 960, 540)
        glClearColor(0.08, 0.10, 0.16, 1.0)

        root_path = Path(__file__).resolve().parent

        self.shader = ShaderProgram(
            root_path / "shaders" / "basic.vert",
            root_path / "shaders" / "basic.frag",
        )

        self.camera = Camera(
            position=(0, 1.5, 6),
            target=(0, 0.2, 0),
            aspect_ratio=960 / 540,
        )

        # Objeto principal da hierarquia.
        self.root = Object3D()

        # Corpo principal: cubo achatado.
        self.body = Object3D(
            Mesh(create_box_geometry(size=1.5))
        )
        self.body.set_scale(1.3, 0.6, 0.9)
        self.root.add(self.body)

        # Pivo responsavel pela articulacao.
        self.pivot = Object3D()
        self.pivot.set_position(0.5, 0.5, 0)
        self.root.add(self.pivot)

        # Peca articulada: cubo fino e comprido.
        self.arm = Object3D(
            Mesh(create_box_geometry(size=1.0))
        )
        self.arm.set_position(0, 0.45, 0)
        self.arm.set_scale(0.25, 0.9, 0.25)
        self.pivot.add(self.arm)

        print("Hierarquia 3D inicializada com sucesso!")

    def update(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Rotaciona todo o conjunto.
        self.root.set_rotation(
            0,
            self.time * 0.6,
            0,
        )

        # Movimenta a peca articulada pelo pivo.
        self.pivot.set_rotation(
            0,
            0,
            math.sin(self.time * 2.0) * 0.45,
        )

        self.shader.use()

        self.shader.set_matrix4(
            "uView",
            self.camera.get_view_matrix(),
        )
        self.shader.set_matrix4(
            "uProjection",
            self.camera.get_projection_matrix(),
        )

        # Renderiza os objetos da hierarquia.
        for obj in self.root.traverse():
            if obj.mesh is not None:
                self.shader.set_matrix4(
                    "uModel",
                    obj.get_world_matrix(),
                )
                obj.mesh.draw()


if __name__ == "__main__":
    app = BesouroCaracolApp()
    app.run()
