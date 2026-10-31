
import pygame

from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_RENDERER,
    GL_SHADING_LANGUAGE_VERSION,
    GL_VENDOR,
    GL_VERSION,
    glClear,
    glClearColor,
    glEnable,
    glGetString,
)


def informacao_opengl(parametro):
    valor = glGetString(parametro)
    return valor.decode("utf-8", errors="replace") if valor else "Indisponível"


def main():
    pygame.init()

    try:
        # Solicita um contexto OpenGL moderno (versão 3.3).
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

        # Cria a janela com suporte ao OpenGL.
        pygame.display.set_mode(
            (960, 540),
            pygame.DOUBLEBUF | pygame.OPENGL,
        )
        pygame.display.set_caption(
            "Computacao Grafica - Besouro e Caracol"
        )

        # Exibe as informações do ambiente gráfico.
        print("=== INFORMACOES OPENGL ===")
        print("Fabricante:", informacao_opengl(GL_VENDOR))
        print("Placa grafica:", informacao_opengl(GL_RENDERER))
        print("Versao OpenGL:", informacao_opengl(GL_VERSION))
        print(
            "Versao GLSL:",
            informacao_opengl(GL_SHADING_LANGUAGE_VERSION),
        )

        glEnable(GL_DEPTH_TEST)

        relogio = pygame.time.Clock()
        executando = True

        while executando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False

            # Define a cor de fundo da janela.
            glClearColor(0.08, 0.10, 0.16, 1.0)

            # Limpa os buffers de cor e profundidade.
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            pygame.display.flip()
            relogio.tick(60)

    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
