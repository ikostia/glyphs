"""
Authors: Nastia Merlits, Kostia Balitsky
"""

from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *

from structures import HORIZONTAL, VERTICAL
from gelements import GDrawing, GZone, GLine, GPoint

class MainWindow(object):
    def __init__(self, drawing):
        self.width, self.height = 800, 600
        self.caption = "Glyph manipulations"
        self.drawing = drawing
        self._init_glut()
        self._init_gl()
        glutMainLoop()

    def _init_gl(self):
        glClearColor(0,0,0,0)
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(2)
        gluOrtho2D(0.0,800.0,0.0,600.0)

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
    drawing = GDrawing(scale=10, width=700, height=500)
    drawing.add_zone(GZone(elements=[GPoint(0, 0),
                           GLine(2, 0, 5, VERTICAL),
                           GLine(4, 0, 5, HORIZONTAL)]))
    drawing.add_zone(GZone(elements=[GPoint(0, 0),
                           GLine(2, 0, 5, VERTICAL),
                           GLine(4, 0, 5, HORIZONTAL)]))

    run_gui(drawing)
