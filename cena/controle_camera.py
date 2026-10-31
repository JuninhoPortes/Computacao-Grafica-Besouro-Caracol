
import math

import pygame


class ControleCamera:
    """Controla a camera em orbita usando o teclado."""

    def __init__(self, camera):
        self.camera = camera

        # Centro em torno do qual a camera gira.
        self.centro = camera.target.copy()

        diferenca = camera.position - self.centro

        # Distancia horizontal em relacao ao centro.
        self.distancia = math.hypot(
            float(diferenca[0]),
            float(diferenca[2]),
        )

        # Angulo inicial da camera.
        self.angulo = math.atan2(
            float(diferenca[0]),
            float(diferenca[2]),
        )

        self.altura = float(camera.position[1])

        # Velocidades controladas pelo tempo decorrido.
        self.velocidade_rotacao = 1.2
        self.velocidade_zoom = 4.0
        self.velocidade_altura = 2.0

    def atualizar(self, delta_time):
        """Atualiza a posicao da camera pelo teclado."""

        teclas = pygame.key.get_pressed()

        # A/D: orbitar horizontalmente.
        if teclas[pygame.K_a]:
            self.angulo -= (
                self.velocidade_rotacao * delta_time
            )

        if teclas[pygame.K_d]:
            self.angulo += (
                self.velocidade_rotacao * delta_time
            )

        # W/S: aproximar e afastar.
        if teclas[pygame.K_w]:
            self.distancia -= (
                self.velocidade_zoom * delta_time
            )

        if teclas[pygame.K_s]:
            self.distancia += (
                self.velocidade_zoom * delta_time
            )

        # Q/E: baixar e elevar a camera.
        if teclas[pygame.K_q]:
            self.altura -= (
                self.velocidade_altura * delta_time
            )

        if teclas[pygame.K_e]:
            self.altura += (
                self.velocidade_altura * delta_time
            )

        # Limites para evitar posicoes inadequadas.
        self.distancia = max(
            5.0, min(16.0, self.distancia)
        )

        self.altura = max(
            1.4, min(7.5, self.altura)
        )

        # Converte a orbita em coordenadas XYZ.
        x = (
            self.centro[0]
            + math.sin(self.angulo) * self.distancia
        )

        z = (
            self.centro[2]
            + math.cos(self.angulo) * self.distancia
        )

        self.camera.position[:] = [
            x,
            self.altura,
            z,
        ]
