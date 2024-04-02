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
class Test(unittest.TestCase):
    def test_rectangle(self):
        rect = Rectangle()

        area = Rectangle.init_length * Rectangle.init_width
        self.assertEqual(rect.area(), area)

        area = rect.length.set_value(12) * Rectangle.init_width
        self.assertEqual(rect.area(), area)

        area = rect.length.set_value(15) * rect.width.set_value(3)
        self.assertEqual(rect.area(), area)

    def test_strip(self):
        rect_count = 5
        strip = Strip()
        rectangles = [Rectangle() for _ in range(rect_count)]
        set_value(strip.rectangles, rectangles)

        area = Rectangle.init_width * Rectangle.init_length * rect_count
        self.assertEqual(strip.area(), area)

        area += rectangles[2].length.set_value(15) * rectangles[2].width.set_value(3) - Rectangle.init_width * Rectangle.init_length
        self.assertEqual(strip.area(), area)

    def test_block(self):
        rect_count = 5
        block = Block()
        rectangles = [Rectangle() for _ in range(rect_count)]
        set_value(block.rectangles, rectangles)

        area = Rectangle.init_width * Rectangle.init_length * rect_count
        volume = area * Block.init_height
        self.assertEqual(block.area(), area)
        self.assertEqual(block.volume(), volume)

        area += rectangles[2].length.set_value(15) * rectangles[2].width.set_value(3) - Rectangle.init_width * Rectangle.init_length
        volume = area * Block.init_height
        self.assertEqual(block.area(), area)
        self.assertEqual(block.volume(), volume)

        volume = area * block.height.set_value(10)
        self.assertEqual(block.area(), area)
        self.assertEqual(block.volume(), volume)
    
    def test_diddle(self):
        rect_count = 5
        block = Block()
        rectangles = [Rectangle() for _ in range(rect_count)]
        set_value(block.rectangles, rectangles)

        for i in range(rect_count):
            self.assertFalse(is_fixed(rectangles[i].length))
            self.assertFalse(is_fixed(rectangles[i].width))

        area = Rectangle.init_width * Rectangle.init_length * rect_count
        area += rectangles[2].length.set_value(15) * rectangles[2].width.set_value(3) - Rectangle.init_width * Rectangle.init_length
        volume = area * block.height.set_value(10)

        self.assertFalse(is_fixed(block.area))
        self.assertFalse(is_fixed(block.volume))
        self.assertEqual(block.area(), area)
        self.assertEqual(block.volume(), volume)

        diddle_area = 0
        diddle_volume = 0
        with graph.DiddleScope(debug_mode=False):
            for i in range(rect_count):
                diddle_area += rectangles[i].length.set_diddle(3) * rectangles[i].width.set_diddle(7)
                self.assertTrue(is_fixed(rectangles[i].length))
                self.assertTrue(is_fixed(rectangles[i].width))
            diddle_volume = block.height.set_diddle(11) * diddle_area

            self.assertFalse(block.area.is_fixed())
            self.assertFalse(block.volume.is_fixed())
            self.assertEqual(block.area(), diddle_area)
            self.assertEqual(block.volume(), diddle_volume)

        # Upon exiting diddle scope, the graph state is reverted to what it was
        self.assertFalse(block.area.is_fixed())
        self.assertFalse(block.volume.is_fixed())
        self.assertEqual(block.area(), area)
        self.assertEqual(block.volume(), volume)
        self.assertNotEqual(block.area(), diddle_area)
        self.assertNotEqual(block.volume(), diddle_volume)
    
    def test_set(self):
        rect_count = 5
        block = Block()
        rectangles = [Rectangle() for _ in range(rect_count)]
        set_value(block.rectangles, rectangles)

        for i in range(rect_count):
            self.assertFalse(is_fixed(rectangles[i].length))
            self.assertFalse(is_fixed(rectangles[i].width))
        
        self.assertFalse(is_fixed(block.height))
        self.assertEqual(block.height(), Block.init_height)

        block.height.set_value(500)
        self.assertTrue(is_fixed(block.height))
        self.assertNotEqual(block.height(), Block.init_height)
        self.assertEqual(block.height(), 500)

        area = Rectangle.init_width * Rectangle.init_length * rect_count
        volume = area * block.height()
        with SetScope({rectangles[2].length: 15, rectangles[2].width: 3, block.height: 10}):
            self.assertTrue(is_fixed(block.height))
            self.assertNotEqual(block.height(), Block.init_height)
            self.assertEqual(block.height(), 10)

            scope_area = area + rectangles[2].length() * rectangles[2].width() - Rectangle.init_width * Rectangle.init_length
            scope_volume = scope_area * block.height()
            self.assertFalse(is_fixed(block.area))
            self.assertFalse(is_fixed(block.volume))
            self.assertEqual(block.area(), scope_area)
            self.assertEqual(block.volume(), scope_volume)

        self.assertTrue(is_fixed(block.height))
        self.assertNotEqual(block.height(), Block.init_height)
        self.assertEqual(block.height(), 500)

        # Upon exiting diddle scope, the graph state is reverted to what it was
        self.assertFalse(block.area.is_fixed())
        self.assertFalse(block.volume.is_fixed())
        self.assertEqual(block.area(), area)
        self.assertEqual(block.volume(), volume)

        block.height.clear_value()
        self.assertFalse(is_fixed(block.height))
        self.assertEqual(block.height(), Block.init_height)

    def test_fixing(self):
        rect_count = 5
        strip = Strip()
        rectangles = [Rectangle() for _ in range(rect_count)]
        set_value(strip.rectangles, rectangles)

        area = Rectangle.init_width * Rectangle.init_length * rect_count
        self.assertEqual(strip.area(), area)

        area += rectangles[2].length.set_value(15) * rectangles[2].width.set_value(3) - Rectangle.init_width * Rectangle.init_length
        fixed_area = strip.area.set_value(2)

        self.assertTrue(strip.area.is_fixed())
        self.assertNotEqual(strip.area(), area)
        self.assertEqual(strip.area(), fixed_area)

        strip.area.clear_value()
        self.assertFalse(strip.area.is_fixed())
        self.assertEqual(strip.area(), area)
        self.assertNotEqual(strip.area(), fixed_area)

if __name__ == '__main__':
    unittest.main()