import numpy as np
import pygame as pg
from numba import njit

from matrix_functions import rotate_x, rotate_y, rotate_z, scale, translate


# Use numba to speed up the operations
@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))


class Object3D:
    def __init__(self, render):
        self.render = render
        self.vertexes = np.array(
            [
                (0, 0, 0, 1),
                (1, 0, 0, 1),
                (1, 1, 0, 1),
                (0, 1, 0, 1),
                (0, 0, 1, 1),
                (1, 0, 1, 1),
                (1, 1, 1, 1),
                (0, 1, 1, 1),
            ]
        )
        self.faces = np.array(
            [
                (0, 1, 2, 3),
                (4, 5, 6, 7),
                (0, 4, 5, 1),
                (1, 5, 6, 2),
                (2, 6, 7, 3),
                (3, 7, 4, 0),
            ]
        )

        self.font = pg.font.SysFont("Arial", 30, bold=True)
        self.color_faces = [(pg.Color("orange"), face) for face in self.faces]
        self.movement_flag, self.draw_vertices = True, False
        self.label = ""

    def draw(self):
        self.screen_projection()

    def screen_projection(self):
        vertices = (
            self.vertexes
            @ self.render.camera.camera_matrix()
            @ self.render.projection.projection_matrix
        )
        vertices /= vertices[:, -1].reshape(-1, 1)

        vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices = vertices[:, :2]

        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            polygon = vertices[face]
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                pg.draw.polygon(self.render.screen, color, polygon, 1)
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color("white"))
                    self.render.screen.blit(text, polygon[-1])

    def translate(self, pos):
        self.vertexes = self.vertexes @ translate(pos)

    def rotate_x(self, theta):
        self.vertexes = self.vertexes @ rotate_x(theta)

    def rotate_y(self, theta):
        self.vertexes = self.vertexes @ rotate_y(theta)

    def scale(self, scale_to):
        self.vertexes = self.vertexes @ scale(scale_to)

    def rotate_z(self, theta):
        self.vertexes = self.vertexes @ rotate_z(theta)
