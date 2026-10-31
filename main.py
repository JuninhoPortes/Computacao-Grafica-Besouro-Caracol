
import math
from pathlib import Path

from OpenGL.GL import (
    GL_DEPTH_TEST,
    glClearColor,
    glEnable,
    glViewport,
)

from framework.core.base import Base
from framework.core.shader_program import ShaderProgram
from framework.core_ext.camera import Camera
from framework.core_ext.mesh import Mesh
from framework.core_ext.object3d import Object3D
from framework.core_ext.scene import Scene
from framework.core_ext.renderer import Renderer
from framework.geometry.box import create_box_geometry


class BesouroCaracolApp(Base):
    """Aplicacao principal de Computacao Grafica."""

    def initialize(self):
        # Configuracoes iniciais do OpenGL.
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, 960, 540)
        glClearColor(0.08, 0.10, 0.16, 1.0)

        root_path = Path(__file__).resolve().parent

        # Programa de shaders.
        self.shader = ShaderProgram(
            root_path / "shaders" / "basic.vert",
            root_path / "shaders" / "basic.frag",
        )

        # Camera em perspectiva.
        self.camera = Camera(
            position=(0, 1.5, 6),
            target=(0, 0.2, 0),
            aspect_ratio=960 / 540,
        )

        # Cena principal e renderizador.
        self.scene = Scene()
        self.renderer = Renderer(self.shader)

        # Objeto raiz do conjunto articulado.
        self.root = Object3D()
        self.scene.add(self.root)

        # Corpo principal.
        self.body = Object3D(
            Mesh(create_box_geometry(size=1.5))
        )
        self.body.set_scale(1.3, 0.6, 0.9)
        self.root.add(self.body)

        # Pivo da articulacao.
        self.pivot = Object3D()
        self.pivot.set_position(0.5, 0.5, 0)
        self.root.add(self.pivot)

        # Peca articulada.
        self.arm = Object3D(
            Mesh(create_box_geometry(size=1.0))
        )
        self.arm.set_position(0, 0.45, 0)
        self.arm.set_scale(0.25, 0.9, 0.25)
        self.pivot.add(self.arm)

        print("Cena e Renderer inicializados com sucesso!")

    def update(self):
        # Rotacao do conjunto completo.
        self.root.set_rotation(
            0,
            self.time * 0.6,
            0,
        )

        # Oscilacao da peca articulada.
        self.pivot.set_rotation(
            0,
            0,
            math.sin(self.time * 2.0) * 0.45,
        )

        # Renderiza toda a cena.
        self.renderer.render(
            self.scene,
            self.camera,
        )


if __name__ == "__main__":
    app = BesouroCaracolApp()
    app.run()
