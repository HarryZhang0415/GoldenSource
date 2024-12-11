import unittest
import GoldenSource.python.common.graph as graph
from GoldenSource.python.common.graph import set_value, is_fixed, SetScope

class Rectangle(graph.GraphObject):
    init_length = 5
    init_width = 5

    @graph.Vertex
    def length(self):
        return self.init_length
    
    @graph.Vertex
    def width(self):
        return self.init_width
    
    @graph.Vertex
    def area(self):
        return self.length() * self.width()
    
class Strip(graph.GraphObject):
    @graph.Vertex
    def rectangles(self):
        return []
    
    @graph.Vertex
    def length(self):
        return sum(rect.length() for rect in self.rectangles())
    
    @graph.Vertex
    def width(self):
        return sum(rect.width() for rect in self.rectangles())
    
    @graph.Vertex
    def area(self):
        return sum(rect.area() for rect in self.rectangles())
    
class Block(Strip):
    init_height = 5

    @graph.Vertex
    def height(self):
        return self.init_height
    
    @graph.Vertex
    def volume(self):
        return self.area() * self.height()
    
# @unittest.skip('Disabled')
def test_rectangle():
    rect = Rectangle()

    area = Rectangle.init_length * Rectangle.init_width
    assert rect.area() == area

    area = rect.length.set_value(12) * Rectangle.init_width
    assert rect.area() == area

    area = rect.length.set_value(15) * rect.width.set_value(3)
    assert rect.area() == area

def test_strip():
    rect_count = 5
    strip = Strip()
    rectangles = [Rectangle() for _ in range(rect_count)]
    set_value(strip.rectangles, rectangles)

    area = Rectangle.init_width * Rectangle.init_length * rect_count
    assert strip.area() == area

    area += rectangles[2].length.set_value(15) * rectangles[2].width.set_value(3) - Rectangle.init_width * Rectangle.init_length
    assert strip.area() == area

def test_block():
    rect_count = 5
    block = Block()
    rectangles = [Rectangle() for _ in range(rect_count)]
    set_value(block.rectangles, rectangles)

    area = Rectangle.init_width * Rectangle.init_length * rect_count
    volume = area * Block.init_height
    assert block.area() == area
    assert block.volume() == volume

    area += rectangles[2].length.set_value(15) * rectangles[2].width.set_value(3) - Rectangle.init_width * Rectangle.init_length
    volume = area * Block.init_height
    assert block.area() == area
    assert block.volume() == volume

    volume = area * block.height.set_value(10)
    assert block.area() == area
    assert block.volume() == volume

def test_diddle():
    rect_count = 5
    block = Block()
    rectangles = [Rectangle() for _ in range(rect_count)]
    set_value(block.rectangles, rectangles)

    for rect in rectangles:
        assert not is_fixed(rect.length)
        assert not is_fixed(rect.width)

    area = Rectangle.init_width * Rectangle.init_length * rect_count
    area += rectangles[2].length.set_value(15) * rectangles[2].width.set_value(3) - Rectangle.init_width * Rectangle.init_length
    volume = area * block.height.set_value(10)

    assert not is_fixed(block.area)
    assert not is_fixed(block.volume)
    assert block.area() == area
    assert block.volume() == volume

    diddle_area = 0
    diddle_volume = 0
    with graph.DiddleScope(debug_mode=False):
        for rect in rectangles:
            diddle_area += rect.length.set_diddle(3) * rect.width.set_diddle(7)
            assert is_fixed(rect.length)
            assert is_fixed(rect.width)
        diddle_volume = block.height.set_diddle(11) * diddle_area

        assert not block.area.is_fixed()
        assert not block.volume.is_fixed()
        assert block.area() == diddle_area
        assert block.volume() == diddle_volume

    assert not block.area.is_fixed()
    assert not block.volume.is_fixed()
    assert block.area() == area
    assert block.volume() == volume
    assert block.area() != diddle_area
    assert block.volume() != diddle_volume

def test_set():
    rect_count = 5
    block = Block()
    rectangles = [Rectangle() for _ in range(rect_count)]
    set_value(block.rectangles, rectangles)

    for rect in rectangles:
        assert not is_fixed(rect.length)
        assert not is_fixed(rect.width)

    assert not is_fixed(block.height)
    assert block.height() == Block.init_height

    block.height.set_value(500)
    assert is_fixed(block.height)
    assert block.height() != Block.init_height
    assert block.height() == 500

    area = Rectangle.init_width * Rectangle.init_length * rect_count
    volume = area * block.height()
    with SetScope({rectangles[2].length: 15, rectangles[2].width: 3, block.height: 10}):
        assert is_fixed(block.height)
        assert block.height() != Block.init_height
        assert block.height() == 10

        scope_area = area + rectangles[2].length() * rectangles[2].width() - Rectangle.init_width * Rectangle.init_length
        scope_volume = scope_area * block.height()
        assert not is_fixed(block.area)
        assert not is_fixed(block.volume)
        assert block.area() == scope_area
        assert block.volume() == scope_volume

    assert is_fixed(block.height)
    assert block.height() != Block.init_height
    assert block.height() == 500

    assert not block.area.is_fixed()
    assert not block.volume.is_fixed()
    assert block.area() == area
    assert block.volume() == volume

    block.height.clear_value()
    assert not is_fixed(block.height)
    assert block.height() == Block.init_height

def test_fixing():
    rect_count = 5
    strip = Strip()
    rectangles = [Rectangle() for _ in range(rect_count)]
    set_value(strip.rectangles, rectangles)

    area = Rectangle.init_width * Rectangle.init_length * rect_count
    assert strip.area() == area

    area += rectangles[2].length.set_value(15) * rectangles[2].width.set_value(3) - Rectangle.init_width * Rectangle.init_length
    fixed_area = strip.area.set_value(2)

    assert strip.area.is_fixed()
    assert strip.area() != area
    assert strip.area() == fixed_area

    strip.area.clear_value()
    assert not strip.area.is_fixed()
    assert strip.area() == area
    assert strip.area() != fixed_area