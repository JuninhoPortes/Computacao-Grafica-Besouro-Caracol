
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_TEXTURE0,
    GL_TEXTURE_2D,
    glActiveTexture,
    glBindTexture,
    glClear,
    glViewport,
)


class Renderer:
    """Renderiza a cena com iluminacao e shadow mapping."""

    def __init__(
        self,
        shader,
        light,
        shadow_map,
        screen_size=(960, 540),
    ):
        self.shader = shader
        self.light = light
        self.shadow_map = shadow_map
        self.screen_size = screen_size

        from framework.material.surface import SurfaceMaterial

        self.default_material = SurfaceMaterial()

    def render(self, scene, camera):
        # PASSAGEM 1: gera a textura de profundidade.
        self.shadow_map.render_depth(scene)

        # PASSAGEM 2: renderiza a cena normalmente.
        glViewport(
            0,
            0,
            self.screen_size[0],
            self.screen_size[1],
        )

        glClear(
            GL_COLOR_BUFFER_BIT |
            GL_DEPTH_BUFFER_BIT
        )

        self.shader.use()

        # Matrizes da camera principal.
        self.shader.set_matrix4(
            "uView",
            camera.get_view_matrix(),
        )

        self.shader.set_matrix4(
            "uProjection",
            camera.get_projection_matrix(),
        )

        self.shader.set_vec3(
            "uCameraPosition",
            camera.position,
        )

        # Iluminacao direcional.
        self.shader.set_vec3(
            "uLightDirection",
            self.light.direction,
        )

        self.shader.set_vec3(
            "uLightColor",
            self.light.color,
        )

        # Matriz de visualizacao da luz.
        self.shader.set_matrix4(
            "uLightViewProjection",
            self.shadow_map.light_view_projection,
        )

        # Unidade 0: textura da superficie.
        # Unidade 1: mapa de profundidade.
        self.shader.set_int("uTexture", 0)
        self.shader.set_int("uShadowMap", 1)

        self.shadow_map.bind(1)

        glActiveTexture(GL_TEXTURE0)

        for obj in scene.traverse():
            if obj.mesh is None:
                continue

            self.shader.set_matrix4(
                "uModel",
                obj.get_world_matrix(),
            )

            # Material do objeto.
            material = (
                obj.material
                if obj.material is not None
                else self.default_material
            )

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

            # Textura comum, quando existente.
            glActiveTexture(GL_TEXTURE0)

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

        # Limpa os bindings de textura utilizados.
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 0)

        glActiveTexture(GL_TEXTURE0 + 1)
        glBindTexture(GL_TEXTURE_2D, 0)

        glActiveTexture(GL_TEXTURE0)
