
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

from personagens.besouro import BesouroMecanico


class BesouroCaracolApp(Base):
    """Aplicacao principal do projeto."""

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
            position=(3.2, 2.4, 5.5),
            target=(0, 0.65, 0),
            aspect_ratio=960 / 540,
        )

        self.scene = Scene()
        self.renderer = Renderer(self.shader)

        # Plataforma do ambiente.
        vertices_chao = create_box_geometry(size=1.0)
        vertices_chao[:, 8:11] = (0.22, 0.27, 0.33)

        chao = Object3D(Mesh(vertices_chao))
        chao.set_position(0, -0.08, 0)
        chao.set_scale(5, 0.16, 5)
        self.scene.add(chao)

        # Primeiro personagem do projeto.
        self.besouro = BesouroMecanico()
        self.scene.add(self.besouro.root)

        print("Besouro mecanico inicializado com sucesso!")

    def update(self):
        # Atualiza as animacoes pelo tempo decorrido.
        self.besouro.update(self.time)

        # Renderiza toda a cena.
        self.renderer.render(
            self.scene,
            self.camera,
        )


if __name__ == "__main__":
    app = BesouroCaracolApp()
    app.run()
