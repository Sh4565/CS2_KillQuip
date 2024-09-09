
import settings

from dataclasses import dataclass


@dataclass
class KillHSV:
    min: tuple = settings.settings.hsv_min
    max: tuple = settings.settings.hsv_max


@dataclass
class BoundingBox:
    top: int = settings.settings.top
    left: int = settings.settings.left
    width: int = settings.settings.width
    height: int = settings.settings.height

    get_dict = {
        'top': top,
        'left': left,
        'width': width,
        'height': height
    }
