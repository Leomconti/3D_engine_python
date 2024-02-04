import math

import pygame as pg

from camera import Camera
from object_3d import Object3D
from projection import Projection
from settings import HEIGHT, WIDTH


class SoftwareRender:

    def __init__(self):
        center_position = (WIDTH // 2, HEIGHT // 2)
        pg.init()
        pg.mouse.set_pos(center_position)
        pg.mouse.set_visible(False)

        self.RES = self.WIDTH, self.HEIGHT = WIDTH, HEIGHT
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.running = True
        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, [0.5, 1, -4])
        self.projection = Projection(self)
        self.object = Object3D(self)
        self.object.translate([0.2, 0.4, 0.2])
        self.object.rotate_y(math.pi / 6)

    def draw(self):
        self.screen.fill(pg.Color("darkslategray"))
        self.object.draw()

    def run(self):
        while True:
            self.draw()
            self.camera.control()
            self.camera.mouse_control()
            [
                exit()
                for i in pg.event.get()
                if i.type == pg.QUIT or (i.type == pg.KEYDOWN and i.key == pg.K_ESCAPE)
            ]
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    app = SoftwareRender()
    app.run()
