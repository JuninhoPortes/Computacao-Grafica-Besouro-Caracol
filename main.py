
from pathlib import Path

import pygame

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
from personagens.caracol import CaracolRobotico

from cena.interacao import ControladorInteracao


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
            position=(4.1, 3.1, 7.7),
            target=(-0.8, 0.7, 0),
            aspect_ratio=960 / 540,
        )

        self.scene = Scene()
        self.renderer = Renderer(self.shader)

        # Plataforma do laboratorio.
        vertices_chao = create_box_geometry(size=1.0)
        vertices_chao[:, 8:11] = (0.22, 0.27, 0.33)

        chao = Object3D(Mesh(vertices_chao))
        chao.set_position(0, -0.08, 0)
        chao.set_scale(7.5, 0.16, 5.5)
        self.scene.add(chao)

        # Personagem 1: Besouro mecanico.
        self.besouro = BesouroMecanico()
        self.scene.add(self.besouro.root)

        # Personagem 2: Caracol robotico.
        self.caracol = CaracolRobotico()
        self.scene.add(self.caracol.root)

        # Controlador de interacao.
        self.interacao = ControladorInteracao()
        self.ultima_fase = None

        print("Cena tridimensional inicializada!")
        print("Interacao coordenada habilitada.")
        print("Pressione R para reiniciar a sequencia.")
        print("Pressione ESC para sair.")

    def handle_event(self, event):
        """Processa comandos especificos da aplicacao."""

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.interacao = ControladorInteracao()
                self.ultima_fase = None

                print("Interacao reiniciada!")

    def update(self):
        # Atualiza a maquina de estados.
        estado = self.interacao.atualizar(
            self.delta_time
        )

        # Identifica mudancas de fase.
        if estado.fase != self.ultima_fase:
            print(f"Fase atual: {estado.fase}")
            self.ultima_fase = estado.fase

        # Atualiza o comportamento do besouro.
        self.besouro.update(
            self.time,
            estado.x_besouro,
            estado.besouro_movendo,
            estado.inspecionando,
        )

        # Atualiza o comportamento do caracol.
        self.caracol.update(
            self.time,
            estado.x_caracol,
            estado.caracol_movendo,
            estado.caracol_alerta,
        )

        # Renderiza a cena.
        self.renderer.render(
            self.scene,
            self.camera,
        )


if __name__ == "__main__":
    app = BesouroCaracolApp()
    app.run()
