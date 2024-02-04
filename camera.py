import pygame as pg

from matrix_functions import *
from settings import HEIGHT, MOUSE_SENSITIVITY, MOVING_SPEED, WIDTH, ROTATION_SPEED


class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100

        self.anglePitch = 0
        self.angleYaw = 0
        self.angleRoll = 0

    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position -= self.right * MOVING_SPEED
        if key[pg.K_d]:
            self.position += self.right * MOVING_SPEED
        if key[pg.K_w]:
            self.position += self.forward * MOVING_SPEED
        if key[pg.K_s]:
            self.position -= self.forward * MOVING_SPEED
        if key[pg.K_q]:
            self.position += self.up * MOVING_SPEED
        if key[pg.K_e]:
            self.position -= self.up * MOVING_SPEED

    def mouse_control(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.camera_yaw(mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.camera_pitch(mouse_dy * MOUSE_SENSITIVITY)

        pg.mouse.set_pos((WIDTH // 2, HEIGHT // 2))

    def camera_yaw(self, angle):
        self.angleYaw += angle

    def camera_pitch(self, angle):
        self.anglePitch += angle

    def axiiIdentity(self):
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

    def camera_update_axii(self):
        rotate = rotate_x(self.anglePitch) @ rotate_y(self.angleYaw)
        self.axiiIdentity()
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_matrix(self):
        self.camera_update_axii()
        return self.translate_matrix() @ self.rotate_matrix()

    def translate_matrix(self):
        x, y, z, w = self.position
        return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-x, -y, -z, 1]])

    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array(
            [[rx, ux, fx, 0], [ry, uy, fy, 0], [rz, uz, fz, 0], [0, 0, 0, 1]]
        )
