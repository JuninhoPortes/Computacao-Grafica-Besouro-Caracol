
from pathlib import Path

from OpenGL.GL import (
    GL_TRUE,
    GL_VERTEX_SHADER,
    GL_FRAGMENT_SHADER,
    glGetUniformLocation,
    glUniformMatrix4fv,
    glUseProgram,
    glUniform1i,
)
from OpenGL.GL.shaders import compileProgram, compileShader


class ShaderProgram:
    """Gerencia um programa de shaders GLSL."""

    def __init__(self, vertex_path, fragment_path):
        vertex_source = Path(vertex_path).read_text(encoding="utf-8")
        fragment_source = Path(fragment_path).read_text(encoding="utf-8")

        self.program = compileProgram(
            compileShader(vertex_source, GL_VERTEX_SHADER),
            compileShader(fragment_source, GL_FRAGMENT_SHADER),
        )

    def use(self):
        glUseProgram(self.program)

    def set_matrix4(self, name, matrix):
        location = glGetUniformLocation(self.program, name)

        if location == -1:
            raise ValueError(f"Uniform nao encontrado: {name}")

        # GL_TRUE permite enviar nossa matriz NumPy em ordem de linhas.
        glUniformMatrix4fv(location, 1, GL_TRUE, matrix)

    
    def set_int(self, name, value):
        """Envia um inteiro para um uniform do shader."""
        location = glGetUniformLocation(
            self.program, name
        )

        if location == -1:
            raise ValueError(
                f"Uniform nao encontrado: {name}"
            )

        glUniform1i(location, int(value))

