"""
Authors: Nastia Merlits, Kostia Balitsky
"""

from settings import HORIZONTAL, VERTICAL, EPS


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "<Point: %r, %r>" % (self.x, self.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        if isinstance(other, Point):
            # scalar product
            return self.x * other.x + self.y * other.y
        else:
            return Point(self.x * other, self.y * other)


class Circle(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def __contains__(self, point):
        return (self.r ** 2 -
                ((point.x - self.x) ** 2 + (point.y - self.y) ** 2)) > -EPS

    def __repr__(self):
        return "<Circle: (%r, %r), %r>" % (self.x, self.y, self.r)


class Line(object):
    def __init__(self, x=0, y=0, l=0):
        self.x = x
        self.y = y
        self.l = l

    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        return self.l

    def __setitem__(self, item, value):
        if item == 0:
            self.x = value
        if item == 1:
            self.y = value
        if item == 2:
            self.l = value


class Glyph(object):
    def __init__(self, orientation):
        self.orientation = orientation
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)

    def __repr__(self):
        return "<%s-Glyph object with %i lines>" %\
                ('H' if self.orientation == HORIZONTAL else 'V',
                len(self.lines), )


class Segment(object):
    """Represent one-dimentional segment"""

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __contains__(self, point):
        """Check whether point lays inside of a segment"""
        return self.start <= point <= self.end

    def __gt__(self, point):
        """Check whether segment lays to the right of a point"""
        return self.start > point

    def __lt__(self, point):
        """Check whether segment lays to the left of a point"""
        return self.end < point

    def __len__(self):
        return self.end - self.start + 1

    def adjacent(self, other):
        """Check whether segment is adjacent to
        another segment or a point.
        """
        if isinstance(other, Segment):
            return self.start - 1 == other.end or self.end + 1 == other.start
        return other == self.start - 1 or other == self.end + 1

    def extend(self, point):
        """Extend segment to the left or to the right with given point"""
        if point == self.start - 1:
            self.start = point
        elif point == self.end + 1:
            self.end = point


class SegmentSequence(object):
    """
    Represent ordered set of one-dimentional disjoint non-adjacent segments.

    This data structure maintains a set of 1D segmens and allows
    one to add an arbitrary point to this set. If the added point lays
    inside of one of the segments, the set remains unchanged. If the point
    is adjacent to one of the segments, the segment extends to include the
    point. Finally, if the point is not adjacent to any segment, the new
    segment containing this point only is created in appropriate place.

    Thus the set of segments is always ordered. Moreover, no two neighbour
    segments are adjacent on a line: if one ends in x, the next one starts
    no earlier than x+2.
    """

    def __init__(self, satellite=None):
        self.satellite = satellite
        self.segments = []

    def _try_to_add_external(self, point):
        """
        Try to add a point if it is not in the boundaries of a current
        segment set.
        """
        if not self.segments:
            self.segments = [Segment(point, point)]
            return True
        if self.segments[-1] < point:
            if self.segments[-1].adjacent(point):
                self.segments[-1].extend(point)
            else:
                self.segments += [Segment(point, point)]
            return True
        if self.segments[0] > point:
            if self.segments[0].adjacent(point):
                self.segments[0].extend(point)
            else:
                self.segments = [Segment(point, point)] + self.segments
            return True
        return False

    def add_point(self, point):
        """Add a new point to the set of segments."""
        if self._try_to_add_external(point):
            return

        left = 0
        right = len(self.segments) - 1
        while right - left > 1:
            mid = (left + right) / 2
            if point in self.segments[mid]:
                left = right = mid
                break
            elif self.segments[mid] > point:
                right = mid
            else:
                left = mid

        if left < right:
            self.segments = (self.segments[:left + 1] +
                        [Segment(point, point)] + self.segments[right:])
            self._try_to_merge(left, left + 1)
            self._try_to_merge(left, left + 1)
            self._try_to_merge(right, right + 1)

    def __repr__(self):
        return "<SegSeq: %r, %r>" %\
            ([(seg.start, seg.end) for seg in self.segments], self.satellite)

    def __iter__(self):
        return iter(self.segments)

    def _try_to_merge(self, ind1, ind2):
        """
        Try to merge segments with indices ``ind1`` and ``ind2``
        into one and return True. Otherwise, return False.
        """
        if ind2 < len(self.segments) and\
                        self.segments[ind1].adjacent(self.segments[ind2]):
            self._merge(ind1, ind2)
            return True
        return False

    def _merge(self, ind1, ind2):
        """Merge segments with indices ``ind1`` and ``ind2``."""
        self.segments = (self.segments[:ind1] +
                        [Segment(self.segments[ind1].start,
                                 self.segments[ind2].end)] +
                        self.segments[ind2 + 1:])
