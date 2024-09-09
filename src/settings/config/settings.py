
import re

from pathlib import Path
from .base import BaseConfig
from .default import DEFAULT_SETTINGS


class SettingsConf(BaseConfig):
    def __init__(self, path_config: Path):
        super().__init__(path_config)

    def _validate_config(self) -> bool:
        required_sections = ['Settings', 'BoundingBox']
        for section in required_sections:
            if section not in self._config:
                return False
        for section, options in DEFAULT_SETTINGS.items():
            for option in options:
                if option not in self._config[section]:
                    return False
        return True

    def _load_defaults(self) -> None:
        self._config.read_dict(DEFAULT_SETTINGS)
        self._save_config()

    @property
    def top(self) -> int:
        return int(self._config.get('BoundingBox', 'top'))

    @property
    def left(self) -> int:
        return int(self._config.get('BoundingBox', 'left'))

    @property
    def width(self) -> int:
        return int(self._config.get('BoundingBox', 'width'))

    @property
    def height(self) -> int:
        return int(self._config.get('BoundingBox', 'height'))

    def set_top(self, value: int) -> None:
        self._config.set('BoundingBox', 'top', str(value))
        self._save_config()

    def set_left(self, value: int) -> None:
        self._config.set('BoundingBox', 'left', str(value))
        self._save_config()

    def set_width(self, value: int) -> None:
        self._config.set('BoundingBox', 'width', str(value))
        self._save_config()

    def set_height(self, value: int) -> None:
        self._config.set('BoundingBox', 'height', str(value))
        self._save_config()

    @property
    def hsv_min(self) -> tuple:
        hsv = self._config.get('Settings', 'HSV_min').split(' ')
        return tuple(map(int, hsv))

    def set_hsv_min(self, hsv: tuple) -> None:
        self._config.set('Settings', 'HSV_min', ' '.join(map(str, hsv)))
        self._save_config()

    @property
    def hsv_max(self) -> tuple:
        hsv = self._config.get('Settings', 'HSV_max').split(' ')
        return tuple(map(int, hsv))

    def set_hsv_max(self, hsv: tuple) -> None:
        self._config.set('Settings', 'HSV_max', ' '.join(map(str, hsv)))
        self._save_config()

    @property
    def path_cs2(self) -> Path:
        return Path(self._config.get('Settings', 'path_CS2'))

    def set_path_cs2(self, path: Path) -> None:
        self._config.set('Settings', 'path_CS2', str(path))
        self._save_config()

    @property
    def messages(self) -> list:
        bad_messages = self._config.get('Settings', 'messages')
        return re.findall(r'(?<=")[^"]+(?=",)', bad_messages)

    def set_messages(self, messages: list) -> None:
        config_messages = ''
        for message in messages:
            config_messages += f'"{message}", '

        self._config.set('Settings', 'messages', config_messages)
        self._save_config()

    @property
    def debug(self) -> bool:
        debug = self._config.get('Debug', 'debug').lower()
        match debug:
            case 'true' | '1':
                return True
            case 'false' | '0' | '':
                return False

    @property
    def print_fps(self) -> bool:
        print_fps = self._config.get('Debug', 'print_fps').lower()
        match print_fps:
            case 'true' | '1':
                return True
            case 'false' | '0' | '':
                return False

    @property
    def screenrecord(self) -> bool:
        screenrecord = self._config.get('Debug', 'screenrecord').lower()
        match screenrecord:
            case 'true' | '1':
                return True
            case 'false' | '0' | '':
                return False

    @property
    def save_frame(self) -> bool:
        save_frame = self._config.get('Debug', 'save_frame').lower()
        match save_frame:
            case 'true' | '1':
                return True
            case 'false' | '0' | '':
                return False

    @property
    def fps_max(self) -> int:
        fps = self._config.get('Settings', 'fps_max')
        match fps:
            case 'false' | '0' | '':
                return False
            case _:
                return int(fps)
