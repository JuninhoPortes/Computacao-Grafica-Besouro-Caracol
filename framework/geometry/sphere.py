
import math

import numpy as np


def create_sphere_geometry(
    radius=1.0,
    stacks=12,
    sectors=20,
    color=(0.2, 0.7, 0.5),
):
    """Cria uma esfera com posicao, normal, UV e cor."""

    vertices = []

    def point(theta, phi):
        nx = math.sin(theta) * math.cos(phi)
        ny = math.cos(theta)
        nz = math.sin(theta) * math.sin(phi)

        u = phi / (2 * math.pi)
        v = 1.0 - theta / math.pi

        return (
            radius * nx,
            radius * ny,
            radius * nz,
            nx, ny, nz,
            u, v,
            *color,
        )

    for i in range(stacks):
        theta0 = math.pi * i / stacks
        theta1 = math.pi * (i + 1) / stacks

        for j in range(sectors):
            phi0 = 2 * math.pi * j / sectors
            phi1 = 2 * math.pi * (j + 1) / sectors

            a = point(theta0, phi0)
            b = point(theta0, phi1)
            c = point(theta1, phi1)
            d = point(theta1, phi0)

            vertices.extend((a, b, c, a, c, d))

    return np.array(vertices, dtype=np.float32).reshape(-1, 11)
