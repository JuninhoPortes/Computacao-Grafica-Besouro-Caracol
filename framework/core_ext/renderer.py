
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    glClear,
)


class Renderer:
    """Responsavel pela renderizacao da cena 3D."""

    def __init__(self, shader):
        self.shader = shader

    def render(self, scene, camera):
        """Renderiza todos os objetos visiveis da cena."""

        # Limpa os buffers antes de desenhar.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Ativa o programa de shaders.
        self.shader.use()

        # Envia as matrizes da camera para a GPU.
        self.shader.set_matrix4(
            "uView",
            camera.get_view_matrix(),
        )

        self.shader.set_matrix4(
            "uProjection",
            camera.get_projection_matrix(),
        )

        # Percorre todos os objetos da cena.
        for obj in scene.traverse():

            # Objetos sem geometria funcionam como grupos.
            if obj.mesh is None:
                continue

            # Envia a transformacao global do objeto.
            self.shader.set_matrix4(
                "uModel",
                obj.get_world_matrix(),
            )

            # Desenha a geometria.
            obj.mesh.draw()
