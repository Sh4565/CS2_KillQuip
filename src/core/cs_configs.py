
import settings

from pathlib import Path


def say_quip(text: str) -> None:
    with open(Path(settings.CS_CFG_PATH, 'quip.cfg'), 'w', encoding='utf-8') as f:
        f.write(f'say {text}')
