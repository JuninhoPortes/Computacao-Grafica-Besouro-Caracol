
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_TEXTURE_2D,
    glBindTexture,
    glClear,
)


class Renderer:
    """Renderiza objetos 3D com cores ou texturas."""

    def __init__(self, shader):
        self.shader = shader

    def render(self, scene, camera):
        # Limpa os buffers.
        glClear(
            GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT
        )

        self.shader.use()

        # Matrizes de camera.
        self.shader.set_matrix4(
            "uView",
            camera.get_view_matrix(),
        )

        self.shader.set_matrix4(
            "uProjection",
            camera.get_projection_matrix(),
        )

        # Unidade de textura utilizada.
        self.shader.set_int("uTexture", 0)

        for obj in scene.traverse():
            if obj.mesh is None:
                continue

            self.shader.set_matrix4(
                "uModel",
                obj.get_world_matrix(),
            )

            # Verifica se o objeto possui textura.
            if obj.texture is not None:
                obj.texture.bind(0)
                self.shader.set_int(
                    "uUseTexture", 1
                )
            else:
                glBindTexture(GL_TEXTURE_2D, 0)
                self.shader.set_int(
                    "uUseTexture", 0
                )

            obj.mesh.draw()

        # Desativa a textura apos a renderizacao.
        glBindTexture(GL_TEXTURE_2D, 0)
