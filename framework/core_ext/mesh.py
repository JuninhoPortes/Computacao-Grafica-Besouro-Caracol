
import ctypes

from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_FALSE,
    GL_FLOAT,
    GL_STATIC_DRAW,
    GL_TRIANGLES,
    glBindBuffer,
    glBindVertexArray,
    glBufferData,
    glDrawArrays,
    glEnableVertexAttribArray,
    glGenBuffers,
    glGenVertexArrays,
    glVertexAttribPointer,
)


class Mesh:
    """Representa uma geometria armazenada na GPU."""

    def __init__(self, vertices):
        self.vertex_count = len(vertices)

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        glBufferData(
            GL_ARRAY_BUFFER,
            vertices.nbytes,
            vertices,
            GL_STATIC_DRAW,
        )

        # Cada vertice possui 11 valores float.
        stride = 11 * 4

        # Local 0: posicao (3 floats)
        # Local 1: normal  (3 floats)
        # Local 2: UV      (2 floats)
        # Local 3: cor     (3 floats)
        attributes = [
            (0, 3, 0),
            (1, 3, 3 * 4),
            (2, 2, 6 * 4),
            (3, 3, 8 * 4),
        ]

        for location, size, offset in attributes:
            glVertexAttribPointer(
                location,
                size,
                GL_FLOAT,
                GL_FALSE,
                stride,
                ctypes.c_void_p(offset),
            )
            glEnableVertexAttribArray(location)

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)
        glBindVertexArray(0)
