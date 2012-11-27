#! /usr/bin/python
"""
Authors: Nastia Merlits, Kostia Balitsky
"""

import structures


class Segment(object):
    """Represent one-dimentional segment"""

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __contains__(self, point):
        """Check whether point lays inside of a segment"""
        if self.start <= point <= self.end:
            return True
        return False

    def __gt__(self, point):
        """Check whether segment lays to the right of a point"""
        if self.start > point:
            return True
        return False

    def __lt__(self, point):
        """Check whether segment lays to the left of a point"""
        if self.end < point:
            return True
        return False

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
        """Extend segment to the left ot to the right with given point"""
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
        if self.segments and self.segments[-1] < point:
            if self.segments[-1].adjacent(point):
                self.segments[-1].extend(point)
            else:
                self.segments += [Segment(point, point)]
            return True
        if self.segments and self.segments[0] > point:
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


class Converter(object):
    def __init__(self):
        pass

    def run(self, glyph):
        if glyph.orientation == structures.HORIZONTAL:
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
        result = structures.Glyph(orientation=not glyph.orientation)
        for level, sequence in seqs.items():
            for segment in sequence:
                line = structures.Line(l=len(segment))
                line[level_coord] = level
                line[dim_coord] = segment.start
                result.add_line(line)

        return result


class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

class ConvexHull(object):
    """
    Graham's scan

    We prefer Graham's scan over Jarvis' march
    because we know nothing about point number in
    a final hull wehreas the initial set of points
    is likely to be partially sorted.
    """

    def __init__(self, point_set):
        self.point_set = point_set
        return NotImplemented


if __name__ == "__main__":
    ss = SegmentSequence(satellite='cool')
    ss.add_point(1)
    ss.add_point(2)
    ss.add_point(4)
    print ss
    ss.add_point(3)
    ss.add_point(2)

    ss.add_point(7)
    ss.add_point(6)
    ss.add_point(9)
    ss.add_point(8)
    print ss
