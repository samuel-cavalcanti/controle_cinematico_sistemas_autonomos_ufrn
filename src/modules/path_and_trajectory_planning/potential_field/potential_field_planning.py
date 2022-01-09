
from ...utils.grid.grid_limits import GridLimits

import numpy as np
from collections import deque

class PotentialFieldPlanning:
    # the number of previous positions used to check oscillations
    OSCILLATIONS_DETECTION_LENGTH = 3

    __potential_map: np.ndarray
    __field_limits:GridLimits
    __motion = [(1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)]

    def __init__(self, potential_map: np.ndarray,field_limits:GridLimits) -> None:
        self.__potential_map = potential_map
        self.__field_limits = field_limits
      

    def __is_valid_move(self, index: tuple[int, int], dx: int, dy: int) -> bool:
        if (dx, dy) == (0, 0):
            False
        if index[0] < 0 or index[1] < 0:
            return False
        try:
            value = self.__get_potencial_value(x=index[0], y=index[1])

            return True

        except IndexError:
            return False

    def __get_potencial_value(self, x: int, y: int) -> float:
        return self.__potential_map[x, y]

    def __move_in_potential_map(self,current_index:tuple[int, int]) -> tuple[int, int]:
        best_move = (-1, -1)
        min_potencial_field_value = float('inf')
        for dx,dy in self.__motion:
            move = (current_index[0] + dx,  current_index[1] + dy)
            if self.__is_valid_move(move, dx, dy):
                potencial_value = self.__get_potencial_value(x=move[0], y=move[1])
                if potencial_value < min_potencial_field_value:
                    min_potencial_field_value = potencial_value
                    best_move = move

        return best_move

    def __index_to_real_pos(self,index:tuple[int, int])->tuple[float,float]:
        
        position_x = index[0] * self.__field_limits.resolution + self.__field_limits.x_min
        position_y = index[1] *self.__field_limits.resolution + self.__field_limits.y_min

        return position_x, position_y

    def __distance_to_goal(self,current_index:tuple[int,int],goal_index: tuple[int, int])->float:
        real_pos_goal =  self.__index_to_real_pos(goal_index)
        real_pos_current_index = self.__index_to_real_pos(current_index) 
      
        return np.hypot(real_pos_goal[0] - real_pos_current_index[0], real_pos_goal[1] - real_pos_current_index[1])

 
    def __oscillations_detection(self,previous_ids:deque[tuple[int,int]],current_id:tuple[int,int])->bool:
        previous_ids.append(current_id)

        if (len(previous_ids) > self.OSCILLATIONS_DETECTION_LENGTH):
            previous_ids.popleft()

        # check if contains any duplicates by copying into a set
        previous_ids_set = set()
        for current_id in previous_ids:
            if current_id in previous_ids_set:
                return True
            else:
                previous_ids_set.add(current_id)
        return False

    def run(self, min_distance: float, start_index: tuple[int, int], goal_index: tuple[int, int]) -> list[tuple[int, int]]:
        path: list[tuple[int, int]] = []
        previous_ids = deque()
        current_index = start_index

        euclidean_distance_to_goal = self.__distance_to_goal(current_index,goal_index)
        
        while euclidean_distance_to_goal >= min_distance:
            current_index = self.__move_in_potential_map(current_index)

            euclidean_distance_to_goal = self.__distance_to_goal(current_index,goal_index)
            path.append(current_index)
        
            if self.__oscillations_detection(previous_ids, current_index):
                print(f"Oscillation detected at ({current_index[0]},{current_index[1]})!")
                break

        return path
