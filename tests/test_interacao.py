
import unittest

from cena.interacao import ControladorInteracao


class TestControladorInteracao(unittest.TestCase):
    """Testes da sequencia coordenada dos personagens."""

    def setUp(self):
        self.controlador = ControladorInteracao()

    def test_estado_inicial(self):
        estado = self.controlador.atualizar(0.0)

        self.assertEqual(estado.fase, "Exploracao")
        self.assertFalse(estado.besouro_movendo)
        self.assertTrue(estado.caracol_movendo)

    def test_fase_aproximacao(self):
        estado = self.controlador.atualizar(3.0)

        self.assertEqual(estado.fase, "Aproximacao")
        self.assertTrue(estado.besouro_movendo)

    def test_caracol_para_na_aproximacao(self):
        estado = self.controlador.atualizar(4.5)

        self.assertEqual(estado.fase, "Aproximacao")
        self.assertFalse(estado.caracol_movendo)
        self.assertTrue(estado.caracol_alerta)

    def test_fase_inspecao(self):
        estado = self.controlador.atualizar(6.0)

        self.assertEqual(estado.fase, "Inspecao")
        self.assertTrue(estado.inspecionando)
        self.assertFalse(estado.besouro_movendo)
        self.assertFalse(estado.caracol_movendo)

    def test_afastamento(self):
        estado = self.controlador.atualizar(9.0)

        self.assertEqual(estado.fase, "Afastamento")
        self.assertTrue(estado.besouro_movendo)
        self.assertFalse(estado.caracol_movendo)

    def test_retomada_caracol(self):
        estado = self.controlador.atualizar(11.0)

        self.assertEqual(estado.fase, "Retomada")
        self.assertFalse(estado.besouro_movendo)
        self.assertTrue(estado.caracol_movendo)

    def test_conclusao(self):
        estado = self.controlador.atualizar(14.0)

        self.assertEqual(estado.fase, "Concluida")
        self.assertFalse(estado.besouro_movendo)
        self.assertFalse(estado.caracol_movendo)

    def test_tempo_pausado(self):
        estado_inicial = self.controlador.atualizar(6.0)

        # Delta time zero simula a pausa da interacao.
        estado_pausado = self.controlador.atualizar(0.0)

        self.assertEqual(estado_inicial, estado_pausado)
        self.assertEqual(estado_pausado.fase, "Inspecao")

    def test_independencia_da_taxa_de_quadros(self):
        controlador_30 = ControladorInteracao()
        controlador_120 = ControladorInteracao()

        # Simula 11 segundos em 30 FPS.
        for _ in range(30 * 11):
            estado_30 = controlador_30.atualizar(1.0 / 30.0)

        # Simula os mesmos 11 segundos em 120 FPS.
        for _ in range(120 * 11):
            estado_120 = controlador_120.atualizar(1.0 / 120.0)

        self.assertEqual(estado_30.fase, estado_120.fase)

        self.assertAlmostEqual(
            estado_30.x_besouro,
            estado_120.x_besouro,
            places=5,
        )

        self.assertAlmostEqual(
            estado_30.x_caracol,
            estado_120.x_caracol,
            places=5,
        )


if __name__ == "__main__":
    unittest.main()
