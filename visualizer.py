
import pygame, sys

from molly.Settings import Settings
from molly.Pathplanner import get_path
from molly.Vec2D import Vec2D
from molly.Circle import Circle

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

    obs1 = Circle(Vec2D(1.5, 1), 0.2)

    circs = [obs1]

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
                            [],
                            circs,
                            start,
                            direction,
                            0,
                            end)

            draw_pos(start)
            draw_pos(end)

            draw_path(path)

            pygame.display.update()

def draw_pos(pos):
    "draw a Vec2D"

    pygame.draw.circle(SCREEN,
                       GREEN,
                       (int(pos.pos_x * PX_PER_METER),
                        int(pos.pos_y * PX_PER_METER)),
                       2,
                       1)

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
