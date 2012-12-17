"""
Authors: Nastia Merlits, Kostia Balitsky
"""

import sys

import reader
from structures import VERTICAL, HORIZONTAL, Point, Glyph, Circle
from algorithm import (Converter, ConvexHull, NaiveEnclosingCircle,
                        LinearEnclosingCircle)
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
    adapter = DrawingAdapter()

    print '-'*50 + '\n'
    
    print 'Initial glyph:'
    print glyph
    print [(line.x, line.y, line.l) for line in glyph.lines]
    print '-'*50 + '\n'
    adapter.add_zone(glyph)

    converted = Converter().run(glyph)
    print 'Converted glyph:'
    print converted
    print [(line.x, line.y, line.l) for line in converted.lines]
    print '-'*50 + '\n'
    adapter.add_zone(converted)

    hull = ConvexHullAdapter(glyph).points
    print 'Convex hull:'
    print hull
    print '-'*50 + '\n'
    adapter.add_zone(hull)

    circle = NaiveEnclosingCircle(hull).circle
    print 'Enclosing circle (by naive algorithm):'
    print circle
    print '-'*50 + '\n'
    adapter.add_zone(glyph, circle)

    # lcircle = LinearEnclosingCircle(hull[2:6]).circle
    # print 'Enclosing circle (by linear algoritm):'
    # print lcircle
    # print '-'*50 + '\n'
    # adapter.add_zone(glyph, lcircle)

    run_gui(adapter.drawing)
