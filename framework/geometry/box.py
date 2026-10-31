
import numpy as np


def create_box_geometry(size=1.5):
    """Cria um cubo com posicao, normal, UV e cor por vertice."""

    h = size / 2

    faces = [
        # Frente
        (
            [(-h, -h, h), (h, -h, h), (h, h, h), (-h, h, h)],
            (0, 0, 1),
            (0.95, 0.30, 0.30),
        ),
        # Tras
        (
            [(h, -h, -h), (-h, -h, -h), (-h, h, -h), (h, h, -h)],
            (0, 0, -1),
            (0.30, 0.75, 0.95),
        ),
        # Esquerda
        (
            [(-h, -h, -h), (-h, -h, h), (-h, h, h), (-h, h, -h)],
            (-1, 0, 0),
            (0.95, 0.75, 0.25),
        ),
        # Direita
        (
            [(h, -h, h), (h, -h, -h), (h, h, -h), (h, h, h)],
            (1, 0, 0),
            (0.35, 0.90, 0.50),
        ),
        # Superior
        (
            [(-h, h, h), (h, h, h), (h, h, -h), (-h, h, -h)],
            (0, 1, 0),
            (0.70, 0.45, 0.95),
        ),
        # Inferior
        (
            [(-h, -h, -h), (h, -h, -h), (h, -h, h), (-h, -h, h)],
            (0, -1, 0),
            (0.85, 0.85, 0.85),
        ),
    ]

    uv = [(0, 0), (1, 0), (1, 1), (0, 1)]
    indices = [0, 1, 2, 0, 2, 3]

    vertices = []

    for corners, normal, color in faces:
        for index in indices:
            vertices.extend(
                (*corners[index], *normal, *uv[index], *color)
            )

    return np.array(vertices, dtype=np.float32).reshape(-1, 11)
