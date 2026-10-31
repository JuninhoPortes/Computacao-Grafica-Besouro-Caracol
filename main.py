
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
from cena.controle_camera import ControleCamera
from framework.core_ext.texture import Texture
from framework.light.directional import DirectionalLight
from framework.material.surface import SurfaceMaterial


class BesouroCaracolApp(Base):
    """Aplicacao principal de Computacao Grafica."""

    def initialize(self):
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, 960, 540)
        glClearColor(0.08, 0.10, 0.16, 1.0)

        root_path = Path(__file__).resolve().parent

        # Shaders.
        self.shader = ShaderProgram(
            root_path / "shaders" / "basic.vert",
            root_path / "shaders" / "basic.frag",
        )

        # Camera em perspectiva.
        self.camera = Camera(
            position=(4.1, 3.1, 7.7),
            target=(-0.8, 0.7, 0),
            aspect_ratio=960 / 540,
        )

        # Controle de camera pelo teclado.
        self.controle_camera = ControleCamera(
            self.camera
        )

        # Cena e renderizador.
        
        self.scene = Scene()

        # Fonte de luz direcional do laboratorio.
        self.luz = DirectionalLight(
            direction=(0.7, 1.0, 0.6),
            color=(1.0, 0.97, 0.90),
        )

        # Renderizador com iluminacao.
        self.renderer = Renderer(
            self.shader,
            self.luz,
        )


        # Plataforma do laboratorio.
        vertices_chao = create_box_geometry(size=1.0)
        vertices_chao[:, 8:11] = (0.22, 0.27, 0.33)

        
        chao = Object3D(Mesh(vertices_chao))
        chao.set_position(0, -0.08, 0)
        chao.set_scale(7.5, 0.16, 5.5)
        
        # Material metalico predominantemente fosco.
        chao.material = SurfaceMaterial(
            ambient=0.40,
            diffuse=0.55,
            specular=0.04,
            shininess=8.0,
        )


        # Aplica uma imagem PNG como textura do piso.
        chao.texture = Texture(
            root_path
            / "texturas"
            / "piso_laboratorio.png"
        )

        self.scene.add(chao)


        # Personagem 1: Besouro mecanico.
        self.besouro = BesouroMecanico()
        self.scene.add(self.besouro.root)

        # Personagem 2: Caracol robotico.
        self.caracol = CaracolRobotico()
        self.scene.add(self.caracol.root)

        # Controlador da interacao.
        self.interacao = ControladorInteracao()

        self.ultima_fase = None

        # Controle independente do tempo de animacao.
        self.tempo_animacao = 0.0

        # Estado da pausa.
        self.pausado = False

        print("Cena tridimensional inicializada!")
        print("Interacao coordenada habilitada.")

        print("\n=== CONTROLES ===")
        print("A / D: Girar camera")
        print("W / S: Aproximar / afastar camera")
        print("Q / E: Baixar / elevar camera")
        print("ESPACO ou P: Pausar / retomar")
        print("R: Reiniciar animacao")
        print("ESC: Sair")

    def handle_event(self, event):
        """Processa os comandos da aplicacao."""

        if event.type != pygame.KEYDOWN:
            return

        # Pausa ou retoma a animacao.
        if event.key in (
            pygame.K_SPACE,
            pygame.K_p,
        ):
            self.pausado = not self.pausado

            if self.pausado:
                print("Animacao pausada.")
            else:
                print("Animacao retomada.")

        # Reinicia toda a sequencia.
        elif event.key == pygame.K_r:
            self.interacao = ControladorInteracao()

            self.tempo_animacao = 0.0
            self.ultima_fase = None
            self.pausado = False

            print("Interacao reiniciada!")

    def update(self):
        # A camera continua funcionando mesmo pausada.
        self.controle_camera.atualizar(
            self.delta_time
        )

        # A animacao so avanca quando nao esta pausada.
        if not self.pausado:
            self.tempo_animacao += self.delta_time
            delta_animacao = self.delta_time
        else:
            delta_animacao = 0.0

        # Atualiza a maquina de estados.
        estado = self.interacao.atualizar(
            delta_animacao
        )

        # Exibe mudancas de fase.
        if estado.fase != self.ultima_fase:
            print(f"Fase atual: {estado.fase}")
            self.ultima_fase = estado.fase

        # Atualiza o besouro.
        self.besouro.update(
            self.tempo_animacao,
            estado.x_besouro,
            estado.besouro_movendo,
            estado.inspecionando,
        )

        # Atualiza o caracol.
        self.caracol.update(
            self.tempo_animacao,
            estado.x_caracol,
            estado.caracol_movendo,
            estado.caracol_alerta,
        )

        # A renderizacao permanece ativa mesmo pausada.
        self.renderer.render(
            self.scene,
            self.camera,
        )


if __name__ == "__main__":
    app = BesouroCaracolApp()
    app.run()
