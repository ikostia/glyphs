HORIZONTAL = False
VERTICAL = True

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
