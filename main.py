"""
Authors: Nastia Merlits, Kostia Balitsky
"""

import sys

import reader
from structures import VERTICAL, HORIZONTAL, Point, Glyph, Circle
from algorithm import Converter, ConvexHull, NaiveEnclosingCircle
from gelements import GDrawing, GZone, GLine, GPoint, GCircle
from drawer import run_gui
import settings

class DrawingAdapter(object):
    def __init__(self):
        self.drawing = GDrawing(scale=settings.SCALE,
                                width=settings.WIDTH,
                                height=settings.HEIGHT)

    def _elements_for_glyph(self, glyph):
        return [GLine(line.x, line.y, line.l, glyph.orientation)
                                                    for line in glyph.lines]

    def _elements_for_point(self, point):
        return [GPoint(point.x, point.y)]

    def _elements_for_circle(self, circle):
        return [GCircle(circle.x, circle.y, circle.r)]

    def _elements_for_list(self, lst):
        elements = []
        for item in lst:
            elements.extend(self._elements_for(item))
        return elements

    def _elements_for(self, item):
        mapping = {
            Glyph: self._elements_for_glyph,
            Point: self._elements_for_point,
            Circle: self._elements_for_circle,
            list: self._elements_for_list}
        return mapping[type(item)](item)

    def add_zone(self, *items):
        elements = []
        for item in items:
            elements.extend(self._elements_for(item))
        self.drawing.add_zone(GZone(elements=elements))


class ConvexHullAdapter(object):
    def __init__(self, glyph):
        points = [Point(line.x, line.y) for line in glyph.lines]
        if glyph.orientation == HORIZONTAL:
            points.extend([Point(line.x + line.l - 1, line.y)
                                for line in glyph.lines])
        else:
            points.extend([Point(line.x, line.y + line.l - 1)
                                for line in glyph.lines])
        self.points = ConvexHull(points).points

if __name__ == "__main__":
    glyph = reader.from_tripples(sys.stdin.read(), HORIZONTAL)
    converted = Converter().run(glyph)
    hull = ConvexHullAdapter(glyph).points
    circle = NaiveEnclosingCircle(hull).circle

    adapter = DrawingAdapter()
    adapter.add_zone(glyph)
    adapter.add_zone(converted)
    adapter.add_zone(hull)
    adapter.add_zone(glyph, circle)

    print '-'*50 + '\n'
    
    print 'Initial glyph:'
    print glyph
    print [(line.x, line.y, line.l) for line in glyph.lines]
    print '-'*50 + '\n'

    print 'Converted glyph:'
    print converted
    print [(line.x, line.y, line.l) for line in converted.lines]
    print '-'*50 + '\n'

    print 'Enclosing circle:'
    print circle
    print '-'*50 + '\n'


    run_gui(adapter.drawing)