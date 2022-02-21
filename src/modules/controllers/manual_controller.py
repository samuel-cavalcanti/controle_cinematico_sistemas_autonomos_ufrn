from typing import Optional
from modules.robots_kinematics.pioneer import PioneerWheelVelocity
import sys


class ManualControllerException(Exception):
    pass


def manual_controller() -> Optional[PioneerWheelVelocity]:

    if sys.platform == "win32":
        return manual_controller_windows()
    elif sys.platform.startswith('linux'):
        raise ManualControllerException(f'Operational system not supported {sys.platform}')
    else:
        raise ManualControllerException(f'Operational system not supported {sys.platform}')


def manual_controller_windows() -> Optional[PioneerWheelVelocity]:
    import msvcrt

    if not msvcrt.kbhit():
        return None

    letra:bytes = msvcrt.getch()

    print("Você apertou a tecla", letra)
    return move(letra.decode())


def move(char: str) -> Optional[PioneerWheelVelocity]:
    if char == 'w':
        print("w")
        return PioneerWheelVelocity(right=1.0, left=1.0)
    elif char == 's':
        print("s")
        return PioneerWheelVelocity(right=-1.0, left=-1.0)
    elif char == 'a':
        print("a")
        return PioneerWheelVelocity(right=1.0, left=0.5)
    elif char == 'd':
        print("d")
        return PioneerWheelVelocity(right=0.5, left=1.0)



def manual_controller_linux() -> Optional[PioneerWheelVelocity]:
    
    return None


