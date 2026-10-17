import unittest
from tools.buffer_slider_model import duration_to_position,position_to_duration

class OriginalSliderModelTests(unittest.TestCase):
    def test_exact_presets(self):
        for i,value in enumerate((10,50,100)):
            self.assertEqual(duration_to_position(value,False),i)
            self.assertEqual(position_to_duration(i,False),value)
    def test_original_midpoints(self):
        for n,expected in [(0,0),(29,0),(30,1),(49,1),(51,1),(74,1),(75,2),(99,2),(100,2),(101,0)]:
            self.assertEqual(duration_to_position(n,False),expected)
    def test_invalid_position(self):
        for n in (-100,-1,3,999):
            self.assertEqual(position_to_duration(n,False),10)
    def test_custom_range(self):
        for n,expected in [(-1,10),(0,10),(9,10),(10,10),(11,11),(65,65),(100,100),(101,100)]:
            self.assertEqual(duration_to_position(n,True),expected)
            self.assertEqual(position_to_duration(n,True),expected)

if __name__=='__main__':unittest.main()
