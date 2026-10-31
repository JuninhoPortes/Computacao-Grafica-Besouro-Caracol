
from PIL import Image

from OpenGL.GL import (
    GL_LINEAR,
    GL_LINEAR_MIPMAP_LINEAR,
    GL_REPEAT,
    GL_RGBA,
    GL_RGBA8,
    GL_TEXTURE0,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_WRAP_S,
    GL_TEXTURE_WRAP_T,
    GL_UNSIGNED_BYTE,
    glActiveTexture,
    glBindTexture,
    glGenTextures,
    glGenerateMipmap,
    glTexImage2D,
    glTexParameteri,
)


class Texture:
    """Carrega uma textura de imagem para a GPU."""

    def __init__(self, image_path):
        with Image.open(image_path) as imagem:
            imagem = imagem.convert("RGBA")

            # Ajusta a orientacao vertical das coordenadas UV.
            imagem = imagem.transpose(
                Image.Transpose.FLIP_TOP_BOTTOM
            )

            largura, altura = imagem.size
            pixels = imagem.tobytes()

        self.texture_id = glGenTextures(1)

        glBindTexture(
            GL_TEXTURE_2D,
            self.texture_id,
        )

        # Define o comportamento nas bordas.
        glTexParameteri(
            GL_TEXTURE_2D,
            GL_TEXTURE_WRAP_S,
            GL_REPEAT,
        )

        glTexParameteri(
            GL_TEXTURE_2D,
            GL_TEXTURE_WRAP_T,
            GL_REPEAT,
        )

        # Define os filtros de amostragem.
        glTexParameteri(
            GL_TEXTURE_2D,
            GL_TEXTURE_MIN_FILTER,
            GL_LINEAR_MIPMAP_LINEAR,
        )

        glTexParameteri(
            GL_TEXTURE_2D,
            GL_TEXTURE_MAG_FILTER,
            GL_LINEAR,
        )

        # Envia os pixels para a GPU.
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA8,
            largura,
            altura,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            pixels,
        )

        # Gera niveis de textura para diferentes distancias.
        glGenerateMipmap(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, 0)

    def bind(self, unit=0):
        """Ativa a textura para renderizacao."""
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(
            GL_TEXTURE_2D,
            self.texture_id,
        )
