from typing import Optional
from modules.robots_kinematics.pioneer import PioneerWheelVelocity

import keyboard



def manual_controller() -> Optional[PioneerWheelVelocity]:
    max_speed = 2.0
    if keyboard.is_pressed('w'):
        print("w")
        return PioneerWheelVelocity(right=max_speed, left=max_speed)
    elif keyboard.is_pressed('s'):
        print("s")
        return PioneerWheelVelocity(right=-max_speed, left=-max_speed)
    elif keyboard.is_pressed('a'):
        print("a")
        return PioneerWheelVelocity(right=max_speed, left=0.5*max_speed)
    elif keyboard.is_pressed('d'):
        print("d")
        return PioneerWheelVelocity(right=0.5*max_speed, left=max_speed)
