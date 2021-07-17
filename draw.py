
"""

Here is where we draw all of the graphics. The ideal would be to define some
function that draws a polygon from a set of points.

"""

import pygame
import numpy as np

import math

import space

pygame.init()

colours = {'black': (0,0,0), 'white':(255,255,255), 'red':(200,50,50),
        'grey':(140, 140, 140), 'light yellow':(255, 255, 0), 'magenta':(150, 0, 100),
        'blue':(0, 0, 255), 'green':(0, 255, 0), '#99FF99':(153, 255, 153),
        '#FF66FF':(255, 102, 255), '#FF9933':(255, 153, 51), '#3399FF':(51, 153, 255),
         'yellow':(214, 214, 0), '#85DFE8':(133, 223, 232), 'very light grey':(200, 200, 200)}
FPS = 60

class Display(object):

    def __init__(self, display_width, display_height, title):
        self.screen = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()

    def event_catcher(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pass
                if event.key == pygame.K_DOWN:
                    pass
                if event.key == pygame.K_RIGHT:
                    pass
                if event.key == pygame.K_LEFT:
                    pass

    def paint(self, objects):
        self.screen.fill(colours['#85DFE8'])
        
        pygame.draw.line(self.screen, colours['#FF66FF'], (space.WIDTH//2 - 10, space.HEIGHT//2),
            (space.WIDTH//2 + 10, space.HEIGHT//2), 2)
        pygame.draw.line(self.screen, colours['#FF66FF'], (space.WIDTH//2, space.HEIGHT//2-10),
            (space.WIDTH//2, space.HEIGHT//2+10), 2)
        

        for object in objects:
            object.draw(self.screen)

        pygame.display.update()
        self.clock.tick(FPS)

class Text(object):

    def __init__(self, text, font=None, fontSize=72):
        self.font = pygame.font.SysFont(font, fontSize)
        self.fontSize = fontSize
        self.main_text = text
        """
        for f in pygame.font.get_fonts():
            print(f)
        """

    def render(self):
        self.texts = self.main_text.split('\n')
        max_text_width = max(map(len, self.texts))
        max_text_height = len(self.texts)

        self.text_widths = [max_text_width for i in range(max_text_height)]
        self.text_heights = [max_text_height - i for i in range(max_text_height)]
        self.imgs = [self.font.render(self.texts[i], True, colours['blue']) for i in range(max_text_height)]

        return list(zip(self.imgs, self.text_widths, self.text_heights))


    def draw(self, screen):
        texts = self.render()
        for text in texts:
            screen.blit(text[0], (space.WIDTH - math.ceil(text[1] * self.fontSize / 2) - 10,
                space.HEIGHT - math.ceil(text[2] * self.fontSize / 1.8) - 10))


class Circle(object):

    def __init__(self, domainPoint, pos, radius, colour, width=0):
        self.domainPoint = domainPoint
        self.pos = pos
        self.radius = radius
        self.colour = colour
        self.width = width

    def getPos(self):
        return self.pos

    def getDomainPoint(self):
        return self.domainPoint

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.pos, self.radius, self.width)


class Ball(object):

    def __init__(self, pos, radius, colour, width=0):
        self.pos = pos
        self.radius = radius
        self.colour = colour
        self.width = width

    def getPos(self):
        return self.pos

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.pos, self.radius, self.width)


class Line(object):

    # we define the origin of the line to be at the constant

    def __init__(self, pos, dir, colour, width=1):
        self.pos = np.array(pos)
        self.dir = np.array(dir)
        self.colour = colour
        self.width = width

    def parameterLine(self, t):
        return self.pos + self.dir * t

    def getGradient(self):
        return self.dir

    def getPos(self):
        return self.pos

    def draw(self, screen):
        pygame.draw.line(screen, self.colour, self.pos, 
            self.pos + self.dir, self.width)
