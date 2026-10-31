
from dataclasses import dataclass


@dataclass(frozen=True)
class SurfaceMaterial:
    """Propriedades de iluminacao de uma superficie."""

    # Intensidade da luz ambiente.
    ambient: float = 0.32

    # Intensidade da reflexao difusa.
    diffuse: float = 0.68

    # Intensidade do brilho especular.
    specular: float = 0.20

    # Concentracao do brilho especular.
    shininess: float = 24.0
