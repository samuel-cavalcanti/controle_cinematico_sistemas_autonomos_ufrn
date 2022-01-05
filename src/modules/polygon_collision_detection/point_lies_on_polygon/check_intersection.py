
Point = tuple[float, float]
Line = tuple[Point, Point]


class CheckInterSection:
    __point:Point
    def __init__(self,point:Point) -> None:
        self.__point = point


    def check(self,line:Line)
