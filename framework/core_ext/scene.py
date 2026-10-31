
from framework.core_ext.object3d import Object3D


class Scene(Object3D):
    """
    Representa a cena tridimensional.

    Funciona como objeto raiz, organizando os
    elementos presentes no ambiente.
    """

    def __init__(self):
        super().__init__()
