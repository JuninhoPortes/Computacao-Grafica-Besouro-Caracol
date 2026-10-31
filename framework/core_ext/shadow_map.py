
import numpy as np

from OpenGL.GL import (
    GL_CLAMP_TO_BORDER,
    GL_DEPTH_ATTACHMENT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_COMPONENT,
    GL_DEPTH_COMPONENT24,
    GL_FLOAT,
    GL_FRAMEBUFFER,
    GL_FRAMEBUFFER_COMPLETE,
    GL_NEAREST,
    GL_NONE,
    GL_TEXTURE0,
    GL_TEXTURE_2D,
    GL_TEXTURE_BORDER_COLOR,
    GL_TEXTURE_COMPARE_MODE,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_WRAP_S,
    GL_TEXTURE_WRAP_T,
    glActiveTexture,
    glBindFramebuffer,
    glBindTexture,
    glCheckFramebufferStatus,
    glClear,
    glDrawBuffer,
    glFramebufferTexture2D,
    glGenFramebuffers,
    glGenTextures,
    glReadBuffer,
    glTexImage2D,
    glTexParameterfv,
    glTexParameteri,
    glViewport,
)

from framework.core.shader_program import ShaderProgram
from framework.core_ext.camera import Camera


class ShadowMap:
    """Gera um mapa de profundidade para sombras direcionais."""

    def __init__(
        self,
        vertex_path,
        fragment_path,
        light_direction,
        resolution=2048,
    ):
        self.resolution = resolution

        self.shader = ShaderProgram(
            vertex_path,
            fragment_path,
        )

        self.direction = np.array(
            light_direction,
            dtype=np.float32,
        )

        comprimento = np.linalg.norm(self.direction)

        if comprimento == 0:
            raise ValueError(
                "A direcao da luz nao pode ser nula."
            )

        self.direction /= comprimento

        # Cria a textura que armazenara as profundidades.
        self.texture_id = glGenTextures(1)

        glBindTexture(
            GL_TEXTURE_2D,
            self.texture_id,
        )

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_DEPTH_COMPONENT24,
            resolution,
            resolution,
            0,
            GL_DEPTH_COMPONENT,
            GL_FLOAT,
            None,
        )

        # Sem interpolacao direta dos valores de profundidade.
        glTexParameteri(
            GL_TEXTURE_2D,
            GL_TEXTURE_MIN_FILTER,
            GL_NEAREST,
        )

        glTexParameteri(
            GL_TEXTURE_2D,
            GL_TEXTURE_MAG_FILTER,
            GL_NEAREST,
        )

        # Fora da textura, considera profundidade maxima.
        glTexParameteri(
            GL_TEXTURE_2D,
            GL_TEXTURE_WRAP_S,
            GL_CLAMP_TO_BORDER,
        )

        glTexParameteri(
            GL_TEXTURE_2D,
            GL_TEXTURE_WRAP_T,
            GL_CLAMP_TO_BORDER,
        )

        glTexParameterfv(
            GL_TEXTURE_2D,
            GL_TEXTURE_BORDER_COLOR,
            np.array(
                [1.0, 1.0, 1.0, 1.0],
                dtype=np.float32,
            ),
        )

        # A comparacao de profundidade sera feita no GLSL.
        glTexParameteri(
            GL_TEXTURE_2D,
            GL_TEXTURE_COMPARE_MODE,
            GL_NONE,
        )

        # Cria um framebuffer exclusivo para profundidade.
        self.framebuffer = glGenFramebuffers(1)

        glBindFramebuffer(
            GL_FRAMEBUFFER,
            self.framebuffer,
        )

        glFramebufferTexture2D(
            GL_FRAMEBUFFER,
            GL_DEPTH_ATTACHMENT,
            GL_TEXTURE_2D,
            self.texture_id,
            0,
        )

        # Este framebuffer nao possui buffer de cores.
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)

        status = glCheckFramebufferStatus(
            GL_FRAMEBUFFER
        )

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindTexture(GL_TEXTURE_2D, 0)

        if status != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError(
                "Framebuffer de sombras incompleto: "
                f"{status}"
            )

        # Matriz usada nas duas passagens.
        self.light_view_projection = (
            self._criar_matriz_luz()
        )

        print("Shadow Map inicializado com sucesso!")

    def _criar_matriz_luz(self):
        """Cria visualizacao e projecao ortografica da luz."""

        centro = np.array(
            [0.0, 0.5, 0.0],
            dtype=np.float32,
        )

        # Posicao virtual usada para observar a cena.
        posicao_luz = centro + self.direction * 12.0

        camera_luz = Camera(
            position=posicao_luz,
            target=centro,
        )

        view = camera_luz.get_view_matrix()

        # Projecao ortografica para uma luz direcional.
        limite = 7.0
        near = 0.1
        far = 40.0

        projection = np.eye(4, dtype=np.float32)

        projection[0, 0] = 1.0 / limite
        projection[1, 1] = 1.0 / limite
        projection[2, 2] = -2.0 / (far - near)
        projection[2, 3] = -(far + near) / (far - near)

        return projection @ view

    def render_depth(self, scene):
        """Primeira passagem: desenha a profundidade da cena."""

        glBindFramebuffer(
            GL_FRAMEBUFFER,
            self.framebuffer,
        )

        glViewport(
            0,
            0,
            self.resolution,
            self.resolution,
        )

        glClear(GL_DEPTH_BUFFER_BIT)

        self.shader.use()

        self.shader.set_matrix4(
            "uLightViewProjection",
            self.light_view_projection,
        )

        # Renderiza todas as geometrias da cena.
        for obj in scene.traverse():
            if obj.mesh is None:
                continue

            self.shader.set_matrix4(
                "uModel",
                obj.get_world_matrix(),
            )

            obj.mesh.draw()

        # Retorna ao framebuffer da janela.
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def bind(self, unit=1):
        """Disponibiliza o mapa de profundidade ao shader."""
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glActiveTexture(GL_TEXTURE0)
