
import math

from framework.core_ext.mesh import Mesh
from framework.core_ext.object3d import Object3D
from framework.geometry.box import create_box_geometry
from framework.geometry.sphere import create_sphere_geometry


class BesouroMecanico:
    """Besouro robotico formado por primitivas geometricas."""

    COR_CORPO = (0.12, 0.35, 0.30)
    COR_CARAPACA = (0.12, 0.68, 0.46)
    COR_CABECA = (0.18, 0.50, 0.40)
    COR_METAL = (0.35, 0.43, 0.48)
    COR_JUNTAS = (0.12, 0.17, 0.20)
    COR_OLHOS = (1.0, 0.80, 0.22)

    def __init__(self):
        self.root = Object3D()

        self.patas = []
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
        self, parent, position, scale, color
    ):
        vertices = create_box_geometry(size=1.0)

        # Substitui as cores das faces pela cor desejada.
        vertices[:, 8:11] = color

        objeto = Object3D(Mesh(vertices))

        objeto.set_position(*position)
        objeto.set_scale(*scale)

        parent.add(objeto)
        return objeto

    def _construir(self):
        # Corpo principal ovalado.
        self._adicionar_esfera(
            self.root,
            (0, 0.78, -0.10),
            (0.76, 0.34, 1.00),
            self.COR_CORPO,
        )

        # Cabeca.
        self._adicionar_esfera(
            self.root,
            (0, 0.80, 0.83),
            (0.43, 0.36, 0.45),
            self.COR_CABECA,
        )

        # Duas metades da carapaca e os olhos.
        for lado in (-1, 1):
            self._adicionar_esfera(
                self.root,
                (lado * 0.34, 1.04, -0.20),
                (0.43, 0.17, 0.86),
                self.COR_CARAPACA,
            )

            self._adicionar_esfera(
                self.root,
                (lado * 0.35, 0.88, 1.15),
                (0.11, 0.12, 0.12),
                self.COR_OLHOS,
            )

        # Linha central entre as metades da carapaca.
        self._adicionar_caixa(
            self.root,
            (0, 1.205, -0.20),
            (0.045, 0.04, 0.84),
            self.COR_JUNTAS,
        )

        # Seis patas roboticas: tres de cada lado.
        for lado in (-1, 1):
            for indice, z in enumerate((-0.65, -0.10, 0.50)):
                pivo = Object3D()
                pivo.set_position(lado * 0.65, 0.62, z)
                self.root.add(pivo)

                self.patas.append((pivo, lado, indice))

                # Segmento superior da pata.
                self._adicionar_caixa(
                    pivo,
                    (lado * 0.27, -0.08, 0),
                    (0.54, 0.11, 0.13),
                    self.COR_METAL,
                )

                # Articulacao da pata.
                junta = Object3D()
                junta.set_position(lado * 0.53, -0.12, 0)
                pivo.add(junta)

                self._adicionar_esfera(
                    junta,
                    (0, 0, 0),
                    (0.11, 0.11, 0.11),
                    self.COR_JUNTAS,
                )

                # Segmento inferior da pata.
                self._adicionar_caixa(
                    junta,
                    (0, -0.23, 0),
                    (0.11, 0.45, 0.13),
                    self.COR_METAL,
                )

        # Duas antenas articuladas.
        for lado in (-1, 1):
            pivo = Object3D()
            pivo.set_position(lado * 0.18, 1.06, 1.14)
            self.root.add(pivo)

            self.antenas.append((pivo, lado))

            # Haste da antena.
            self._adicionar_caixa(
                pivo,
                (lado * 0.10, 0.28, 0.12),
                (0.06, 0.54, 0.06),
                self.COR_METAL,
            )

            # Sensor na ponta da antena.
            self._adicionar_esfera(
                pivo,
                (lado * 0.10, 0.57, 0.12),
                (0.10, 0.10, 0.10),
                self.COR_OLHOS,
            )

    def update(self, tempo):
        """Atualiza os movimentos do besouro."""

        # Deslocamento e oscilacao do corpo.
        self.root.set_position(
            0,
            math.sin(tempo * 6.0) * 0.02,
            math.sin(tempo * 0.65) * 0.28,
        )

        self.root.set_rotation(
            0,
            math.sin(tempo * 0.5) * 0.15,
            0,
        )

        # Movimento alternado das patas.
        for pivo, lado, indice in self.patas:
            fase = indice * math.pi

            if lado == 1:
                fase += math.pi

            movimento = math.sin(
                tempo * 6.0 + fase
            ) * 0.22

            pivo.set_rotation(
                0,
                movimento,
                -lado * 0.04,
            )

        # Oscilacao das antenas.
        for pivo, lado in self.antenas:
            movimento = math.sin(
                tempo * 3.0 + lado
            ) * 0.14

            pivo.set_rotation(
                0,
                0,
                lado * 0.15 + movimento,
            )
