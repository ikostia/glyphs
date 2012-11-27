import itertools
import structures

class ImpoperInputFormat(Exception):
    pass

def from_tripples(input, orientation):
    glyph = structures.Glyph(orientation)
    nums = [long(item) for item in input.split()]
    tripples = [ nums[i:i+3]
                    for i in xrange(0, len(nums), 3)]
    if len(tripples) !=0 and len(tripples[-1]) != 3:
        raise ImpoperInputFormat("Total number of integers "
                                 "should be multiple of 3")
    for x, y, l in tripples:
        glyph.add_line(structures.Line(x, y, l))
    return glyph
