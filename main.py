#! /usr/bin/python
"""
Authors: Nastia Merlits, Kostia Balitsky
"""

import sys
import reader
import structures
import algorithm

if __name__ == "__main__":
    glyph = reader.from_tripples(sys.stdin.read(),
                                 structures.VERTICAL)
    print glyph
    print [(line.x, line.y, line.l) for line in glyph.lines]
    converted = algorithm.Converter().run(glyph)
    print converted
    print [(line.x, line.y, line.l) for line in converted.lines]