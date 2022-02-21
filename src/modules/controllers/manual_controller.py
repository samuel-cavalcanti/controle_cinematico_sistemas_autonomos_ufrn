from tkinter import N
from typing import Optional
from modules.robots_kinematics.pioneer import PioneerWheelVelocity
import sys


class ManualControllerException(Exception):
    pass


def manual_controller() -> Optional[PioneerWheelVelocity]:

    if sys.platform == "win32":
        return manual_controller_windows()
    elif sys.platform.startswith('linux'):
        return manual_controller_linux()
    else:
        raise ManualControllerException(f'Operational system not supported {sys.platform}')


def manual_controller_windows() -> Optional[PioneerWheelVelocity]:
    import msvcrt

    if not msvcrt.kbhit():
        return None

    letra = msvcrt.getch()

    print("Você apertou a tecla", letra)

    if letra == b'w':
        print("w")
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

    return None


def manual_controller_linux() -> Optional[PioneerWheelVelocity]:

    return None
