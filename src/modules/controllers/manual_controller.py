from modules.robots_kinematics.pioneer import PioneerWheelVelocity
import keyboard

def manual_controller(letra: bytes) -> PioneerWheelVelocity: 
    if letra == b'w':
        print ("w")
        return PioneerWheelVelocity(right=1.0, left=1.0)
    elif letra == b's':
        print("s")
        return PioneerWheelVelocity(right=-1.0, left=-1.0)
    elif letra == b'a':
        print("a")
        return PioneerWheelVelocity(right=1.0, left=0.5)
    elif letra == b'd':
        print("d")
        return PioneerWheelVelocity(right=0.5, left=1.0)