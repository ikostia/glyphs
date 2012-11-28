"""
Authors: Nastia Merlits, Kostia Balitsky
"""

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

from gelements import GDrawing, GZone, GLine, GPoint, GCircle
from settings import WIDTH, HEIGHT, SCALE, HORIZONTAL, VERTICAL


class MainWindow(object):
    def __init__(self, drawing):
        self.width, self.height = WIDTH, HEIGHT
        self.caption = "Glyph manipulations"
        self.drawing = drawing
        self._init_glut()
        self._init_gl()
        glutMainLoop()

    def _init_gl(self):
        glClearColor(0, 0, 0, 0)
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(2)
        gluOrtho2D(0.0, 1. * self.width, 0.0, 1. * self.height)

    def _init_glut(self):
        glutInit()
        glutInitWindowSize(self.width, self.height)
        glutInitDisplayMode(GLUT_RGB | GLUT_SINGLE)
        glutCreateWindow(self.caption)
        glutDisplayFunc(self.on_draw)

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        if self.drawing:
           self.drawing.draw()
        glFlush()


def run_gui(drawing):
    window = MainWindow(drawing)


if __name__ == "__main__":
    drawing = GDrawing(scale=SCALE, width=WIDTH, height=HEIGHT)
    drawing.add_zone(GZone(elements=[GPoint(0, 0),
                           GLine(2, 0, 5, VERTICAL),
                           GLine(4, 0, 5, HORIZONTAL)]))
    drawing.add_zone(GZone(elements=[GPoint(0, 0),
                           GLine(2, 0, 5, VERTICAL),
                           GLine(4, 0, 5, HORIZONTAL)]))
    drawing.add_zone(GZone(elements=[GCircle(10, 10, 6)]))

    run_gui(drawing)
