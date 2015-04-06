
import pygame, sys

from molly.Settings import Settings, STAIRS
from molly.Pathplanner import get_path
from molly.Vec2D import Vec2D
from molly.Circle import Circle
from molly.Tangent import Tangent
from molly.Polygon import Polygon

PX_PER_METER = 400
SETTINGS = Settings()
WIDTH = int(SETTINGS.width * PX_PER_METER)
HEIGHT = int(SETTINGS.height * PX_PER_METER)
#BACKGROUND = pygame.image.load("")
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)

def main():
    "draw loop"

    start = Vec2D(0.1, 0.1)
    end = Vec2D(2.1, 1.1)
    direction = Vec2D(0, 0.1)

    obs1 = Circle(Vec2D(1.5, 0.75), 0.2)
    #obs2 = Circle(Vec2D(0.9, 0.6), 0.2)

    corner1 = Circle(Vec2D(), 0.1)
    corner2 = Circle(Vec2D(0.5, 0), 0.1)
    side1 = Tangent(Vec2D(0, -0.1), corner1, -1, Vec2D(0.5, -0.1), corner2, 1)
    side2 = Tangent(Vec2D(0, 0.1), corner1, 1, Vec2D(0.5, 0.1), corner2, -1)

    poly1 = Polygon([corner1, corner2], [side1, side2]) + Vec2D(0.15, 0.3)

    circs = [obs1]
    polys = [STAIRS, poly1]

    paused = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

        if not paused:
            SCREEN.fill(BLACK)
            #SCRREN.blit(BACKGROUND, (0, 0))

            path = get_path(SETTINGS,
                            polys,
                            circs,
                            start,
                            direction,
                            0,
                            end)

            draw_pos(start)
            draw_pos(end)

            draw_env(SETTINGS, circs, polys)

            draw_path(path)

            pygame.display.update()

def draw_env(settings, circ_obs, poly_obs):
    "draw all the things!"

    for circ in settings.static_circ_obs:
        draw_circle(circ)

    for poly in settings.static_poly_obs:
        draw_poly(poly)

    for circ in circ_obs:
        draw_circle(circ)

    for poly in poly_obs:
        draw_poly(poly)

def draw_pos(pos):
    "draw a Vec2D"

    pygame.draw.circle(SCREEN,
                       GREEN,
                       (int(pos.pos_x * PX_PER_METER),
                        int(pos.pos_y * PX_PER_METER)),
                       2,
                       1)

def draw_circle(circle):
    "draw a Circle"

    pygame.draw.circle(SCREEN,
                       RED,
                       (int(circle.pos.pos_x * PX_PER_METER),
                        int(circle.pos.pos_y * PX_PER_METER)),
                       int(circle.radius * PX_PER_METER),
                       1)

def draw_line(pos1, pos2):
    "draw line from pos1 to pos2"
    pygame.draw.line(SCREEN,
                     RED,
                     (int(pos1.pos_x * PX_PER_METER),
                      int(pos1.pos_y * PX_PER_METER)),
                     (int(pos2.pos_x * PX_PER_METER),
                      int(pos2.pos_y * PX_PER_METER)),
                     1)

def draw_poly(poly):
    "draw polygon"

    for circle in poly.corners:
        draw_circle(circle)

    for tan in poly.sides:
        draw_line(tan.start_pos, tan.end_pos)

def draw_path(path):
    "draw waypoints of path"
    if not path:
        return

    prev = path[0]

    for curr in path[1:]:
        pygame.draw.line(SCREEN,
                         BLUE,
                         (int(prev[0].pos_x * PX_PER_METER),
                          int(prev[0].pos_y * PX_PER_METER)),
                         (int(curr[0].pos_x * PX_PER_METER),
                          int(curr[0].pos_y * PX_PER_METER)),
                         1)

        # draw speed vector
        #pygame.draw.line(SCREEN,
        #                 BLUE,
        #                 (int(prev[0].pos_x * PX_PER_METER),
        #                  int(prev[0].pos_y * PX_PER_METER)),
        #                 (int((prev[0] + prev[1]).pos_x * PX_PER_METER),
        #                  int((prev[0] + prev[1]).pos_y * PX_PER_METER)),
        #                 1)

        prev = curr

if __name__ == "__main__":
    main()
