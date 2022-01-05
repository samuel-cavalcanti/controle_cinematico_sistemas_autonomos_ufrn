import unittest

from src.modules.polygon_collision_detection.point_lies_on_polygon.check_intersection import CheckInterSection


class CheckIntersectionTestCase(unittest.TestCase):

    check_intersection = CheckInterSection(point=(0.5, 0.5))

    def test_horizontal_line(self):

        not_intersect_line = ((0.0, 0.3), (0.4, 0.3))

        intersect_line = ((0.0, 0.5), (0.5, 0.5))

        result = self.check_intersection.check(not_intersect_line)

        self.assertFalse(result.is_intersect, f'Line {intersect_line} should not intersect')
        self.assertTrue(result.is_horizontal_line, f'Line {not_intersect_line} is Horizontal')

        result = self.check_intersection.check(intersect_line)

        self.assertTrue(result.is_intersect, f'Line {intersect_line} should intersect')
        self.assertTrue(result.is_horizontal_line, f'Line {intersect_line} is Horizontal')

        checker = CheckInterSection(point=(-1, 10))

        line = ((0.0, 0.0), (10.0, 0.0))
        result = checker.check(line)

        self.assertTrue(result.is_horizontal_line, f'Line {line} is Horizontal')
        self.assertFalse(result.is_intersect, f'Line {line} should intersect')



    def test_vertical_line(self):

        intersect_line = ((1, 0), (1, 7))

        result = self.check_intersection.check(intersect_line)

        self.assertTrue(result.is_intersect, f'Line {intersect_line} should intersect')
        self.assertFalse(result.is_horizontal_line, f'Line {intersect_line} is not Horizontal')

        not_intersect_line = ((0.5, 1.5), (0.5, 2.5))

        result = self.check_intersection.check(not_intersect_line)

        self.assertFalse(result.is_intersect, f'Line {not_intersect_line} should not intersect')
        self.assertFalse(result.is_horizontal_line, f'Line {not_intersect_line} is not Horizontal')

    def test_diagonal_line(self):

        intersect_line = ((0.0, 0.0), (2.0, 2.0))

        result = self.check_intersection.check(intersect_line)

        self.assertTrue(result.is_intersect, f'Line {intersect_line} should intersect')
        self.assertFalse(result.is_horizontal_line, f'Line {intersect_line} is not Horizontal')

        not_intersect_line = ((0.0, 0.0), (2.5, 3.5))

        result = self.check_intersection.check(not_intersect_line)

        self.assertFalse(result.is_intersect, f'Line {not_intersect_line} should not intersect')
        self.assertFalse(result.is_horizontal_line, f'Line {not_intersect_line} is not Horizontal')
