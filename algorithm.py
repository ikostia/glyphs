"""
Authors: Nastia Merlits, Kostia Balitsky
"""

import random

from settings import HORIZONTAL, VERTICAL, EPS
from structures import SegmentSequence, Glyph, Line, Point, Circle


class Converter(object):
    def __init__(self):
        pass

    def run(self, glyph):
        if glyph.orientation == HORIZONTAL:
            level_coord = 1
        else:
            level_coord = 0
        dim_coord = 1 - level_coord

        seqs = {}
        for line in glyph.lines:
            for point in xrange(line[dim_coord], line[dim_coord] + line.l):
                seq = seqs.get(point, SegmentSequence())
                seq.add_point(line[level_coord])
                seqs[point] = seq

        level_coord, dim_coord = dim_coord, level_coord
        result = Glyph(orientation=not glyph.orientation)
        for level, sequence in seqs.items():
            for segment in sequence:
                line = Line(l=len(segment))
                line[level_coord] = level
                line[dim_coord] = segment.start
                result.add_line(line)

        return result


class ConvexHull(object):
    def __init__(self, points):
        points.sort(key=lambda p: p.x)
        self.pivot, points = points[0], points[1:]
        points.sort(lambda p1, p2: self.angle_cmp(p1, p2))

        if len(points) < 2:
            self.hull = [pivot] + points
            return

        hull = [self.pivot, points[0]]
        for i in xrange(1, len(points)):
            while len(hull) >= 2 and self.counterclockwise(hull[-2], hull[-1], points[i]) <= 0:
                hull.pop()
            hull.append(points[i])

        self.points = hull

    def sign(self, x):
        return 1 if x > 0 else 0 if x == 0 else -1

    def angle_cmp(self, p1, p2):
        return -self.sign(self.counterclockwise(self.pivot, p1, p2))

    def cross(self, v1, v2):
        return v1.x * v2.y - v1.y * v2.x

    def counterclockwise(self, p1, p2, p3):
        """
        Check whether a turn from (p1, p2) to (p1, p3) is counter clockwise.

        If it is so, the return value is > 0, if the turn is clockwise, the 
        return value is < 0. If vectors are collinear, the return value is 0.
        """
        return self.cross(Point(p2.x - p1.x, p2.y - p1.y), Point(p3.x - p1.x, p3.y - p1.y))


class BaseEnclosingCircle(object):
    def distance(self, p1, p2):
        return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5

    def middle(self, *points):
        x, y = 0, 0
        for point in points:
            x, y = x + point.x, y + point.y
        x, y = x * 1. / len(points), y * 1. / len(points)
        return Point(x, y)

    def circle_on_diameter(self, p1, p2):
        center = self.middle(p1, p2)
        rad = self.distance(p1, p2) / 2.
        return Circle(center.x, center.y, rad)

    def circle_on_triangle(self, p1, p2, p3):
        a = self.distance(p1, p2)
        b = self.distance(p1, p3)
        c = self.distance(p2, p3)
        p = (a + b + c) / 2.
        s = (p * (p - a) * (p - b) * (p - c)) ** 0.5
        try:
            rad = a*b*c / 4. / s
        except ZeroDivisionError, e:
            print 'Points: ', p1, p2, p3
            print 'Sides: ', a, b, c
            print 'Half-perim: ', p
            raise

        alpha_a = a * a / 8. / s / s * ((p1 - p3) * (p2 - p3))
        alpha_b = b * b / 8. / s / s * ((p1 - p2) * (p3 - p2))
        alpha_c = c * c / 8. / s / s * ((p2 - p1) * (p3 - p1))

        center = p3 * alpha_a + p2 * alpha_b + p1 * alpha_c

        return Circle(center.x, center.y, rad)

    def is_enclosing(self, circle, points):
        return all([point in circle for point in points])


class LinearEnclosingCircle(BaseEnclosingCircle):
    def __init__(self, points):
        print points
        pointnum = len(points)
        self.iterations = 0
        #random.shuffle(points)
        self.circle = self.build_circle(points, [])
        print 'LEC required %r iterations on %r points' % (self.iterations, pointnum)
        if self.is_enclosing(self.circle, points):
            print 'Circle is actually enclosing'
        else:
            print 'Circle is not an enclosing one'

    def by_bound(self, points_on_bound):
        # print 'BB: ', points_on_bound
        if len(points_on_bound) == 0:
            #print 'Building empty'
            return Circle(0, 0, 0)
        if len(points_on_bound) == 1:
            #print 'Buildin on center'
            return Circle(points_on_bound[0].x, points_on_bound[0].y, 0)
        if len(points_on_bound) == 2:
            #print 'Building on diameter'
            return self.circle_on_diameter(points_on_bound[0], points_on_bound[1])
        #print 'Building on triangle'
        return self.circle_on_triangle(points_on_bound[0],
                                       points_on_bound[1],
                                       points_on_bound[2])

    def build_circle(self, points, support):
        # print 'BC: ', points, support
        self.iterations += 1

        if points:
            ind = random.randint(0, len(points) - 1)
            points[ind], points[-1] = points[-1], points[ind]
            
            circle = None
            if len(support) == 3:
                circle = self.by_bound(support)
            
            if not circle:
                circle = self.build_circle(points[:-1], support)
                
            
            if points[-1] in circle:
                return circle
            else:
                support.append(points[-1])
                if len(support) > 3:
                    points = [support[0]] + points
                    support = support[1:]
                return self.build_circle(points[:-1], support)
        else:
            return self.by_bound(support)


class NaiveEnclosingCircle(BaseEnclosingCircle):
    """Naive O(n^4) implementation of minimum enclosing circle"""

    def __init__(self, points):
        if len(points) == 1:
            self.circle = Circle(points[0].x, points[0].y, 0)
            return
        
        if len(points) == 2:
            self.circle = self.circle_on_diameter(points[0], points[1])
            return

        j1, j2 = 0, 1
        for i1 in xrange(len(points)):
            for i2 in xrange(i1 + 1, len(points)):
                if self.distance(points[i1], points[i2]) >\
                                self.distance(points[j1], points[j2]):
                    j1, j2 = i1, i2

        circle_ = self.circle_on_diameter(points[j1], points[j2])
        radius_threshold = circle_.r
        if self.is_enclosing(circle_, points):
            self.circle = circle_
            return

        circle = None
        for i1 in xrange(len(points)):
            for i2 in xrange(i1 + 1, len(points)):
                for i3 in xrange(i2 + 1, len(points)):
                    circle_ = self.circle_on_triangle(points[i1],
                                                      points[i2],
                                                      points[i3])
                    if circle_.r - radius_threshold > -EPS  and\
                                (not circle or circle.r - circle_.r > -EPS) and\
                                self.is_enclosing(circle_, points):
                        circle = circle_
        self.circle = circle

        if self.circle is None:
            raise Exception('No idea how, but we did not find an enclosing circle.')


if __name__ == "__main__":
    points = [Point(3, 11), Point(10, 4), Point(16, 1), Point(20, 0)]
    lc = LinearEnclosingCircle(points)

    exit()

    points = [Point(0, 1), Point(0, 0), Point(1, 1), Point(1, 0), Point(.5, .5),
              Point(.7, .7), Point(.5, 1), Point(1, .5), Point(.5, -1)]
    ch = ConvexHull(points)
    print ch.points

    ec = NaiveEnclosingCircle(ch.points)
    lc = LinearEnclosingCircle(ch.points)
    print ec.circle
    print lc.circle

    from math import pi, sin, cos
    cos45 = cos(pi / 4)
    cos60 = cos(pi / 3)
    sin60 = sin(pi / 3)
    points = [Point(0., 1.), Point(1., 0.),
              Point(1. + cos45, 1 + cos45),
              Point(1. + sin60, 1. - cos60)]
    naive = NaiveEnclosingCircle(points)
    linear = LinearEnclosingCircle(points)
    print naive.circle
    print linear.circle
