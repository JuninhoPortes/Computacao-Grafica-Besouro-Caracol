
import math
import unittest

import numpy as np

from framework.core_ext.object3d import Object3D
from framework.geometry.box import create_box_geometry
from framework.geometry.sphere import create_sphere_geometry


class TestGeometrias(unittest.TestCase):
    """Verifica a estrutura das geometrias tridimensionais."""

    def test_geometria_cubo(self):
        vertices = create_box_geometry()

        # Seis faces, dois triangulos por face.
        self.assertEqual(vertices.shape, (36, 11))

        # Confirma a presenca de normais unitarias.
        normais = vertices[:, 3:6]
        comprimentos = np.linalg.norm(normais, axis=1)

        np.testing.assert_allclose(
            comprimentos,
            1.0,
            atol=1e-5,
        )

    def test_geometria_esfera(self):
        vertices = create_sphere_geometry(
            stacks=8,
            sectors=12,
        )

        # Cada divisao gera dois triangulos.
        self.assertEqual(
            vertices.shape,
            (8 * 12 * 6, 11),
        )

        # Confirma os vetores normais da esfera.
        normais = vertices[:, 3:6]
        comprimentos = np.linalg.norm(normais, axis=1)

        np.testing.assert_allclose(
            comprimentos,
            1.0,
            atol=1e-5,
        )

    def test_coordenadas_uv(self):
        vertices = create_sphere_geometry()

        uv = vertices[:, 6:8]

        self.assertTrue(np.all(uv >= 0.0))
        self.assertTrue(np.all(uv <= 1.0))


class TestTransformacoes(unittest.TestCase):
    """Verifica as matrizes e hierarquias de objetos."""

    def test_translacao(self):
        objeto = Object3D()
        objeto.set_position(2.0, 1.0, 3.0)

        origem = np.array([0, 0, 0, 1])

        resultado = objeto.get_world_matrix() @ origem

        np.testing.assert_allclose(
            resultado,
            [2.0, 1.0, 3.0, 1.0],
            atol=1e-5,
        )

    def test_escala(self):
        objeto = Object3D()
        objeto.set_scale(2.0, 3.0, 4.0)

        ponto = np.array([1, 1, 1, 1])

        resultado = objeto.get_world_matrix() @ ponto

        np.testing.assert_allclose(
            resultado,
            [2.0, 3.0, 4.0, 1.0],
            atol=1e-5,
        )

    def test_hierarquia_com_rotacao(self):
        pai = Object3D()
        filho = Object3D()

        pai.set_rotation(0, math.pi / 2, 0)
        filho.set_position(0, 0, 2)

        pai.add(filho)

        origem = np.array([0, 0, 0, 1])

        resultado = filho.get_world_matrix() @ origem

        # A rotacao do pai afeta a posicao global do filho.
        np.testing.assert_allclose(
            resultado,
            [2.0, 0.0, 0.0, 1.0],
            atol=1e-5,
        )


if __name__ == "__main__":
    unittest.main()
