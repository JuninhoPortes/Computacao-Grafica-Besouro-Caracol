
import math

import numpy as np


class Camera:
    """Camera com projecao em perspectiva."""

    def __init__(
        self,
        position=(0, 1.5, 5),
        target=(0, 0, 0),
        aspect_ratio=16 / 9,
        fov=60,
    ):
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.aspect_ratio = aspect_ratio
        self.fov = fov

    def get_view_matrix(self):
        forward = self.target - self.position
        forward /= np.linalg.norm(forward)

        up = np.array([0, 1, 0], dtype=np.float32)

        right = np.cross(forward, up)
        right /= np.linalg.norm(right)

        true_up = np.cross(right, forward)

        matrix = np.eye(4, dtype=np.float32)

        matrix[0, :3] = right
        matrix[1, :3] = true_up
        matrix[2, :3] = -forward

        matrix[0, 3] = -np.dot(right, self.position)
        matrix[1, 3] = -np.dot(true_up, self.position)
        matrix[2, 3] = np.dot(forward, self.position)

        return matrix

    def get_projection_matrix(self):
        near = 0.1
        far = 100.0

        scale = 1.0 / math.tan(math.radians(self.fov) / 2)

        matrix = np.zeros((4, 4), dtype=np.float32)

        matrix[0, 0] = scale / self.aspect_ratio
        matrix[1, 1] = scale
        matrix[2, 2] = (far + near) / (near - far)
        matrix[2, 3] = (2 * far * near) / (near - far)
        matrix[3, 2] = -1.0

        return matrix
