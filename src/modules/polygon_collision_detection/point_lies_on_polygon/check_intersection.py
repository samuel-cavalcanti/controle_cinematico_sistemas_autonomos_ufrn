from enum import Enum, auto
Point = tuple[float, float]
Line = tuple[Point, Point]


class Orientation(Enum):
    Collinear = auto()
    Clockwise = auto()
    Counterclockwise = auto()


class CheckInterSection:
    __point: tuple[float, float]
    __extreme_point: Point

    def __init__(self, point: Point) -> None:
        self.__point = point
        self.__extreme_point = (10000, self.__point[1])

    def do_intersect(self, edge: Line) -> bool:

        infinity_horizontal_line = (self.__point, self.__extreme_point)
        # Find the four orientations needed for
        # general and special cases
        o1 = self.orientation(line=edge, point=self.__point)
        o2 = self.orientation(line=edge, point=self.__extreme_point)
        o3 = self.orientation(line=infinity_horizontal_line, point=edge[0])
        o4 = self.orientation(line=infinity_horizontal_line, point=edge[1])

        # General case
        if (o1 != o2) and (o3 != o4):
            return True

        # Special Cases
        # p1, q1 and p2 are collinear and
        # p2 lies on segment p1q1
        if o1 == Orientation.Collinear and self.on_segment(line=(edge[0], self.__point), point=edge[1]):
            return True

        # p1, q1 and p2 are collinear and
        # q2 lies on segment p1q1
        if o2 == Orientation.Collinear and self.on_segment(line=(edge[0], self.__extreme_point), point=edge[1]):
            return True

        # p2, q2 and p1 are collinear and
        # p1 lies on segment p2q2
        if o3 == Orientation.Collinear and self.on_segment(line=(self.__point, edge[0]), point=self.__extreme_point):
            return True

        # p2, q2 and q1 are collinear and
        # q1 lies on segment p2q2
        if o4 == Orientation.Collinear and self.on_segment(line=(self.__point, edge[1]), point=self.__extreme_point):
            return True

        return False

    @staticmethod
    def orientation(line: Line, point: Point) -> Orientation:
        point_a = line[0]
        point_b = line[1]

        line_delta_y = point_b[1] - point_a[1]
        line_delta_x = point_b[0] - point_a[0]

        delta_x = point[0] - point_b[0]
        delta_y = point[1] - point_b[1]

        val = (line_delta_y*delta_x) - (line_delta_x*delta_y)

        if val == 0:
            return Orientation.Collinear
        if val > 0:
            return Orientation.Clockwise
        else:
            return Orientation.Counterclockwise

    @staticmethod
    def on_segment(line: Line, point: Point) -> bool:
        point_a = line[0]
        point_b = line[1]

        is_on_x = (point_b[0] <= max(point_a[0], point[0])) and (point_b[0] >= min(point_a[0], point[0]))

        is_on_y = (point_b[1] <= max(point_a[1], point[1])) and (point_b[1] >= min(point_a[1], point[1]))

        return is_on_x and is_on_y
