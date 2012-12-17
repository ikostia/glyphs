"""
Authors: Nastia Merlits, Kostia Balitsky
"""

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

from math import pi, cos, sin
import structures
from settings import (BORDER_COLOR, FILL_COLOR, HORIZONTAL, VERTICAL,
                        XOFFSET, YOFFSET, SCALE)

class GElement(object):
    def draw(self, x, y, scale):
        return NotImplemented

class GPoint(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, x, y, scale):
        left = x + self.x * scale
        right = left + scale - 1
        top = y + self.y * scale
        bottom = top + scale - 1

        glColor3f(*FILL_COLOR)
        glBegin(GL_POLYGON)
        glVertex2i(left, top)
        glVertex2i(right, top)
        glVertex2i(right, bottom)
        glVertex2i(left, bottom)
        glEnd()
        glColor3f(*BORDER_COLOR)
        glBegin(GL_LINE_LOOP)
        glVertex2i(left, top)
        glVertex2i(right, top)
        glVertex2i(right, bottom)
        glVertex2i(left, bottom)
        glEnd()

    @property
    def max_x(self):
        return self.x

    @property
    def max_y(self):
        return self.y


class GLine(GElement):
    def __init__(self, x, y, l, orientation):
        self.x = x
        self.y = y
        self.l = l
        self.orientation = orientation

    @property
    def max_x(self):
        if self.orientation == HORIZONTAL:
            return self.x + self.l - 1
        return self.x

    @property
    def max_y(self):
        if self.orientation == VERTICAL:
            return self.y + self.l - 1
        return self.y

    def draw(self, x, y, scale):
        left = x + self.x * scale
        right = left + scale - 1
        top = y + self.y * scale
        bottom = top + scale - 1

        if self.orientation == HORIZONTAL:
            right = right + scale * (self.l - 1)
        else:
            bottom = bottom + scale * (self.l - 1)
        
        glColor3f(*FILL_COLOR)
        glBegin(GL_POLYGON)
        glVertex2i(left, top)
        glVertex2i(right, top)
        glVertex2i(right, bottom)
        glVertex2i(left, bottom)
        glEnd()
        glColor3f(*BORDER_COLOR)
        glBegin(GL_LINE_LOOP)
        glVertex2i(left, top)
        glVertex2i(right, top)
        glVertex2i(right, bottom)
        glVertex2i(left, bottom)
        glEnd()



class GCircle(GElement):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    @property
    def max_x(self):
        return max(self.x + self.r - 1, 2 * self.r)

    @property
    def max_y(self):
        return max(self.y + self.r - 1, 2 * self.r)

    def draw(self, x, y, scale):
        cx, cy = x + self.x * scale + scale/2, y + self.y * scale + scale/2
        step = pi / 1000
        rad = self.r * scale
        glColor3f(*BORDER_COLOR)
        glBegin(GL_LINE_LOOP)
        angle = pi
        while angle > -pi:
            glVertex2i(int(cx + cos(angle) * rad),
                       int(cy + sin(angle) * rad))
            angle = angle - step
        glEnd()


class GZone(GElement):
    def __init__(self, elements=[]):
        self.elements = elements

    def add_element(self, element):
        self.element.append(element)

    def draw(self, x, y, scale):
        for element in self.elements:
            element.draw(x, y, scale)

    @property
    def width(self):
        return max([el.max_x for el in self.elements])

    @property
    def height(self):
        return max([el.max_y for el in self.elements])


class GDrawing(object):
    def __init__(self, scale, width, height):
        self.xoffset = XOFFSET
        self.yoffset = YOFFSET
        self.width = width
        self.height = height
        self.scale = scale
        self.zones = []

    def add_zone(self, zone):
        self.zones.append(zone)

    def draw(self):
        left, top = self.xoffset, self.yoffset
        right, bottom = left, top
        for zone in self.zones:
            zw, zh = self.scale * zone.width, self.scale * zone.height
            if left + zw > self.width - self.xoffset:
                top = bottom + self.yoffset
                left = self.xoffset
            zone.draw(left, top, self.scale)
            left = left + zw + self.xoffset
            if top + zh > bottom:
                bottom = top + zh
