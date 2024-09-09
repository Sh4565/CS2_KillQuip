
import os

from pathlib import Path
from .config import SettingsConf


if os.path.isfile(Path(__file__).resolve()):
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
else:
    BASE_DIR = Path(__file__).resolve().parent.parent


settings = SettingsConf(Path(BASE_DIR, 'settings.cfg'))


CS_PATH = settings.path_cs2
CS_CFG_PATH = Path(CS_PATH, 'game', 'csgo', 'cfg')
