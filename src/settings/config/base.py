
import configparser

from pathlib import Path
from abc import ABC, abstractmethod


class BaseConfig(ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BaseConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self, path_config: Path):
        self._path_config = path_config
        self._config = configparser.ConfigParser()

        if not self._path_config.exists():
            self._load_defaults()
            self._save_config()
            raise FileNotFoundError("Файл конфигурации не найден. Загружены дефолтные настройки.")

        self._config.read(self._path_config, encoding='utf-8')

        if not self._validate_config():
            self._load_defaults()
            self._save_config()
            raise ValueError("Файл конфигурации поврежден. Загружены дефолтные настройки.")

    @abstractmethod
    def _validate_config(self) -> bool:
        pass

    @abstractmethod
    def _load_defaults(self) -> None:
        pass

    def _save_config(self) -> None:
        with open(self._path_config, 'w') as configfile:
            self._config.write(configfile)

    def get_config(self):
        """Возвращает текущую конфигурацию."""
        return self._config
