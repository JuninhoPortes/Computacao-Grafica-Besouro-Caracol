
import math
import numpy as np


class Object3D:
    """Objeto 3D com transformacoes e hierarquia de filhos."""

    def __init__(self, mesh=None):
        self.mesh = mesh
        self.parent = None
        self.children = []

        self.position = np.zeros(3, dtype=np.float32)
        self.rotation = np.zeros(3, dtype=np.float32)
        self.scale = np.ones(3, dtype=np.float32)

    def add(self, child):
        """Adiciona um objeto filho a esta hierarquia."""
        if child is self or child.parent is not None:
            raise ValueError("Objeto invalido ou ja possui pai.")

        self.children.append(child)
        child.parent = self

    def set_position(self, x, y, z):
        self.position[:] = [x, y, z]

    def set_rotation(self, x, y, z):
        """Define as rotacoes em radianos."""
        self.rotation[:] = [x, y, z]

    def set_scale(self, x, y, z):
        self.scale[:] = [x, y, z]

    def get_local_matrix(self):
        """Calcula a matriz de transformacao local."""
        x, y, z = self.rotation

        cx, sx = math.cos(x), math.sin(x)
        cy, sy = math.cos(y), math.sin(y)
        cz, sz = math.cos(z), math.sin(z)

        translation = np.eye(4, dtype=np.float32)
        translation[:3, 3] = self.position

        rotation_x = np.array([
            [1, 0, 0, 0],
            [0, cx, -sx, 0],
            [0, sx, cx, 0],
            [0, 0, 0, 1],
        ], dtype=np.float32)

        rotation_y = np.array([
            [cy, 0, sy, 0],
            [0, 1, 0, 0],
            [-sy, 0, cy, 0],
            [0, 0, 0, 1],
        ], dtype=np.float32)

        rotation_z = np.array([
            [cz, -sz, 0, 0],
            [sz, cz, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ], dtype=np.float32)

        scaling = np.diag([
            self.scale[0],
            self.scale[1],
            self.scale[2],
            1.0,
        ]).astype(np.float32)

        return (
            translation
            @ rotation_z
            @ rotation_y
            @ rotation_x
            @ scaling
        )

    def get_world_matrix(self):
        """Combina a transformacao local com a do objeto pai."""
        local = self.get_local_matrix()

        if self.parent is None:
            return local

        return self.parent.get_world_matrix() @ local

    def traverse(self):
        """Percorre todos os objetos da hierarquia."""
        yield self

        for child in self.children:
            yield from child.traverse()
