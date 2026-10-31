
from dataclasses import dataclass


@dataclass
class EstadoInteracao:
    """Representa o estado atual dos personagens."""

    fase: str
    x_besouro: float
    x_caracol: float
    besouro_movendo: bool
    caracol_movendo: bool
    inspecionando: bool = False
    caracol_alerta: bool = False


class ControladorInteracao:
    """Coordena as acoes do besouro e do caracol."""

    def __init__(self):
        self.tempo = 0.0

    @staticmethod
    def interpolar(inicio, fim, progresso):
        """Interpola valores entre duas posicoes."""
        progresso = max(0.0, min(1.0, progresso))

        return inicio + (fim - inicio) * progresso

    def atualizar(self, delta_time):
        """Atualiza a sequencia usando o tempo decorrido."""

        self.tempo += max(0.0, delta_time)
        t = self.tempo

        # FASE 1: Caracol explora a plataforma.
        if t < 2.0:
            progresso = t / 2.0

            return EstadoInteracao(
                fase="Exploracao",
                x_besouro=2.25,
                x_caracol=self.interpolar(
                    -1.8, -1.5, progresso
                ),
                besouro_movendo=False,
                caracol_movendo=True,
            )

        # FASE 2: Besouro se aproxima.
        if t < 5.2:
            progresso = (t - 2.0) / 3.2

            # Caracol para quando o besouro esta perto.
            progresso_caracol = min(
                progresso / 0.65, 1.0
            )

            caracol_parou = progresso >= 0.65

            return EstadoInteracao(
                fase="Aproximacao",
                x_besouro=self.interpolar(
                    2.25, 1.55, progresso
                ),
                x_caracol=self.interpolar(
                    -1.5, -1.27, progresso_caracol
                ),
                besouro_movendo=True,
                caracol_movendo=not caracol_parou,
                caracol_alerta=caracol_parou,
            )

        # FASE 3: Besouro realiza a inspecao.
        if t < 7.8:
            return EstadoInteracao(
                fase="Inspecao",
                x_besouro=1.55,
                x_caracol=-1.27,
                besouro_movendo=False,
                caracol_movendo=False,
                inspecionando=True,
                caracol_alerta=True,
            )

        # FASE 4: Besouro libera a passagem.
        if t < 10.2:
            progresso = (t - 7.8) / 2.4

            return EstadoInteracao(
                fase="Afastamento",
                x_besouro=self.interpolar(
                    1.55, 2.25, progresso
                ),
                x_caracol=-1.27,
                besouro_movendo=True,
                caracol_movendo=False,
                caracol_alerta=True,
            )

        # FASE 5: Caracol retoma o percurso.
        if t < 13.0:
            progresso = (t - 10.2) / 2.8

            return EstadoInteracao(
                fase="Retomada",
                x_besouro=2.25,
                x_caracol=self.interpolar(
                    -1.27, -0.7, progresso
                ),
                besouro_movendo=False,
                caracol_movendo=True,
            )

        # Sequencia concluida.
        return EstadoInteracao(
            fase="Concluida",
            x_besouro=2.25,
            x_caracol=-0.7,
            besouro_movendo=False,
            caracol_movendo=False,
        )
