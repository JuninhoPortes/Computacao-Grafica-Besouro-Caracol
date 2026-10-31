
from dataclasses import dataclass


@dataclass(frozen=True)
class DirectionalLight:
    """Representa uma fonte de iluminacao direcional."""

    # Vetor apontando da superficie para a fonte de luz.
    direction: tuple = (0.7, 1.0, 0.6)

    # Cor da iluminacao.
    color: tuple = (1.0, 0.97, 0.90)
