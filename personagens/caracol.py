
import math

from framework.core_ext.mesh import Mesh
from framework.core_ext.object3d import Object3D
from framework.geometry.box import create_box_geometry
from framework.geometry.sphere import create_sphere_geometry


class CaracolRobotico:
    """Caracol robotico construido com formas geometricas."""

    COR_CORPO = (0.20, 0.57, 0.68)
    COR_CABECA = (0.35, 0.75, 0.78)
    COR_CONCHA = (0.95, 0.63, 0.28)
    COR_PAINEL = (0.78, 0.46, 0.20)
    COR_ESPIRAL = (0.27, 0.22, 0.25)
    COR_METAL = (0.42, 0.50, 0.58)
    COR_OLHOS = (1.00, 0.87, 0.30)
    COR_SENSORES = (0.32, 0.91, 1.00)

    def __init__(self):
        self.root = Object3D()
        self.antenas = []

        self._construir()

    def _adicionar_esfera(
        self, parent, position, scale, color
    ):
        vertices = create_sphere_geometry(color=color)
        objeto = Object3D(Mesh(vertices))

        objeto.set_position(*position)
        objeto.set_scale(*scale)

        parent.add(objeto)
        return objeto

    def _adicionar_caixa(
        self, parent, position, scale, color,
        rotacao_x=0.0,
    ):
        vertices = create_box_geometry(size=1.0)
        vertices[:, 8:11] = color

        objeto = Object3D(Mesh(vertices))

        objeto.set_position(*position)
        objeto.set_scale(*scale)
        objeto.set_rotation(rotacao_x, 0, 0)

        parent.add(objeto)
        return objeto

    def _construir(self):
        # Corpo alongado que desliza sobre o chao.
        self._adicionar_esfera(
            self.root,
            (0, 0.38, 0.14),
            (0.55, 0.29, 1.02),
            self.COR_CORPO,
        )

        # Trilhos laterais decorativos.
        for lado in (-1, 1):
            self._adicionar_caixa(
                self.root,
                (lado * 0.50, 0.30, 0.12),
                (0.08, 0.13, 1.30),
                self.COR_METAL,
            )

        # Concha principal.
        self._adicionar_esfera(
            self.root,
            (0, 0.96, -0.28),
            (0.63, 0.65, 0.66),
            self.COR_CONCHA,
        )

        # Paineis nas duas laterais da concha.
        for lado in (-1, 1):
            self._adicionar_esfera(
                self.root,
                (lado * 0.58, 0.96, -0.28),
                (0.10, 0.53, 0.55),
                self.COR_PAINEL,
            )

            # Desenha uma espiral geometrica em cada painel.
            self._construir_espiral(lado)

        # Pivo que permite movimentar a cabeca.
        self.cabeca_pivo = Object3D()
        self.cabeca_pivo.set_position(0, 0.44, 0.76)
        self.root.add(self.cabeca_pivo)

        # Cabeca arredondada.
        self._adicionar_esfera(
            self.cabeca_pivo,
            (0, 0.20, 0.20),
            (0.42, 0.42, 0.42),
            self.COR_CABECA,
        )

        for lado in (-1, 1):
            # Olhos na parte frontal da cabeca.
            self._adicionar_esfera(
                self.cabeca_pivo,
                (lado * 0.20, 0.24, 0.56),
                (0.10, 0.11, 0.10),
                self.COR_OLHOS,
            )

            # Pivo independente para cada antena.
            pivo = Object3D()
            pivo.set_position(
                lado * 0.23, 0.46, 0.36
            )
            self.cabeca_pivo.add(pivo)

            self.antenas.append((pivo, lado))

            # Haste da antena.
            self._adicionar_caixa(
                pivo,
                (0, 0.28, 0),
                (0.075, 0.56, 0.075),
                self.COR_METAL,
            )

            # Sensor luminoso na ponta.
            self._adicionar_esfera(
                pivo,
                (0, 0.61, 0),
                (0.12, 0.12, 0.12),
                self.COR_SENSORES,
            )

    def _construir_espiral(self, lado):
        """Cria o desenho da espiral usando segmentos."""

        centro_y = 0.96
        centro_z = -0.28

        quantidade = 20
        voltas = 3.7 * math.pi

        def ponto(indice):
            proporcao = indice / quantidade
            angulo = proporcao * voltas

            raio = 0.38 - proporcao * 0.31

            y = centro_y + raio * math.sin(angulo)
            z = centro_z + raio * math.cos(angulo)

            return y, z

        for indice in range(quantidade):
            y1, z1 = ponto(indice)
            y2, z2 = ponto(indice + 1)

            dy = y2 - y1
            dz = z2 - z1

            comprimento = math.hypot(dy, dz)
            angulo_x = math.atan2(dz, dy)

            # Cada caixa representa um segmento da espiral.
            self._adicionar_caixa(
                self.root,
                (
                    lado * 0.69,
                    (y1 + y2) / 2,
                    (z1 + z2) / 2,
                ),
                (0.065, comprimento, 0.065),
                self.COR_ESPIRAL,
                rotacao_x=angulo_x,
            )

    def update(self, tempo):
        """Atualiza o deslizamento e as articulacoes."""

        # Deslocamento inicial de demonstracao.
        # A interacao coordenada sera adicionada depois.
        self.root.set_position(
            -2.0,
            math.sin(tempo * 3.0) * 0.015,
            math.sin(tempo * 0.6) * 0.15,
        )

        # Pequena mudanca de orientacao.
        self.root.set_rotation(
            0,
            math.sin(tempo * 0.45) * 0.11,
            0,
        )

        # Movimento sutil da cabeca.
        self.cabeca_pivo.set_rotation(
            math.sin(tempo * 1.8) * 0.07,
            0,
            0,
        )

        # Oscilacao independente das antenas.
        for pivo, lado in self.antenas:
            movimento = math.sin(
                tempo * 2.8 + lado
            ) * 0.14

            pivo.set_rotation(
                movimento * 0.5,
                0,
                lado * 0.12 + movimento,
            )
