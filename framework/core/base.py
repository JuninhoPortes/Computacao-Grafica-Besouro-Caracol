
import pygame


class Base:
    """Classe base para aplicações gráficas com Pygame e OpenGL."""

    def __init__(
        self,
        screen_size=(960, 540),
        title="Computacao Grafica - Besouro e Caracol",
    ):
        pygame.init()

        # Configura um contexto OpenGL 3.3 Core.
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_MAJOR_VERSION, 3
        )
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_MINOR_VERSION, 3
        )
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK,
            pygame.GL_CONTEXT_PROFILE_CORE,
        )

        pygame.display.set_mode(
            screen_size,
            pygame.DOUBLEBUF | pygame.OPENGL,
        )
        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()
        self.running = True

        # Tempo entre quadros e tempo total da aplicação.
        self.delta_time = 0.0
        self.time = 0.0

    def initialize(self):
        """Implementado pela aplicação para preparar a cena."""
        raise NotImplementedError

    def update(self):
        """Implementado pela aplicação para atualizar e renderizar."""
        raise NotImplementedError

    
    def handle_event(self, event):
        """Permite tratar eventos especificos da aplicacao."""
        pass


    def run(self):
        """Executa o ciclo principal da aplicação."""
        try:
            self.initialize()

            while self.running:
                # Calcula o tempo decorrido em segundos.
                self.delta_time = self.clock.tick(60) / 1000.0
                self.time += self.delta_time

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.running = False

                    # Encaminha o evento para a aplicacao.
                    self.handle_event(event)

                if not self.running:
                    break

                self.update()
                pygame.display.flip()

        finally:
            pygame.quit()
