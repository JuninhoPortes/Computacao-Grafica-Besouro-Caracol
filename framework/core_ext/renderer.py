
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_TEXTURE0,
    GL_TEXTURE_2D,
    glActiveTexture,
    glBindTexture,
    glClear,
)

from framework.light.directional import DirectionalLight
from framework.material.surface import SurfaceMaterial


class Renderer:
    """Renderiza objetos com materiais e luz direcional."""

    def __init__(self, shader, light=None):
        self.shader = shader

        self.light = (
            light if light is not None
            else DirectionalLight()
        )

        # Material utilizado quando o objeto nao possui um proprio.
        self.default_material = SurfaceMaterial()

    def render(self, scene, camera):
        # Limpa os buffers da janela.
        glClear(
            GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT
        )

        self.shader.use()

        # Matrizes da camera.
        self.shader.set_matrix4(
            "uView",
            camera.get_view_matrix(),
        )

        self.shader.set_matrix4(
            "uProjection",
            camera.get_projection_matrix(),
        )

        # Posicao da camera para reflexao especular.
        self.shader.set_vec3(
            "uCameraPosition",
            camera.position,
        )

        # Configura a iluminacao direcional.
        self.shader.set_vec3(
            "uLightDirection",
            self.light.direction,
        )

        self.shader.set_vec3(
            "uLightColor",
            self.light.color,
        )

        # Unidade de textura utilizada.
        self.shader.set_int("uTexture", 0)
        glActiveTexture(GL_TEXTURE0)

        # Renderiza os objetos da cena.
        for obj in scene.traverse():
            if obj.mesh is None:
                continue

            # Matriz global do objeto.
            self.shader.set_matrix4(
                "uModel",
                obj.get_world_matrix(),
            )

            # Seleciona o material da superficie.
            material = (
                obj.material
                if obj.material is not None
                else self.default_material
            )

            # Envia as propriedades do material.
            self.shader.set_float(
                "uMaterialAmbient",
                material.ambient,
            )

            self.shader.set_float(
                "uMaterialDiffuse",
                material.diffuse,
            )

            self.shader.set_float(
                "uMaterialSpecular",
                material.specular,
            )

            self.shader.set_float(
                "uMaterialShininess",
                material.shininess,
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

            # Desenha a geometria.
            obj.mesh.draw()

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 0)
