
import sys
import time
import random
import argparse
import keyboard

from pathlib import Path

import settings

from data.models import BoundingBox
from core.cs_configs import say_quip
from utils import area_selection, find_color

from core.vision import Vision


def select_area() -> None:
    """Выбор и сохранение области экрана для обработки."""
    print('Нажмите сочетание клавиш Shift + Win + S и выделите карту (с зазорами)')
    top, left, width, height = area_selection()

    settings.settings.set_top(top)
    settings.settings.set_left(left)
    settings.settings.set_width(width)
    settings.settings.set_height(height)

    print(f'\nКоординаты области успешно записаны!\n'
          f'top: {top}, left: {left}, width: {width}, height: {height}')


def find_and_save_color() -> None:
    """Поиск цвета и сохранение его значений в настройках."""
    print('Сейчас появятся два окна.\n'
          'В первом окне - ползунки для редактирования фильтра по цвету.\n'
          'Во втором - примененный фильтр на области экрана, где белый цвет - это искомый контур.')

    hsv_min, hsv_max = find_color(BoundingBox.get_dict, settings.settings.hsv_min, settings.settings.hsv_max)

    if hsv_max and hsv_min:
        settings.settings.set_hsv_min(hsv_min)
        settings.settings.set_hsv_max(hsv_max)
        print(f'HSV_min: {hsv_min}, HSV_max: {hsv_max}')


def set_game_path(arg_path) -> None:
    """Установка пути к корневой директории игры."""
    path = arg_path if arg_path is not True else input(
        'Введите абсолютный путь к файлам игры.\n'
        r'Пример пути: X:\SteamLibrary\steamapps\common\Counter-Strike Global Offensive'
        '\nВведите путь к файлам: ')

    settings.settings.set_path_cs2(Path(path))
    print(f'Путь успешно добавлен!\nПуть к корневой директории игры: {path}')


def set_messages(arg_messages) -> None:
    """Добавление сообщений для отображения в игре."""
    if arg_messages is True:
        print('Вводите сообщения, после каждого ввода нажимайте Enter.\n'
              'Когда закончите вводить сообщения, просто нажмите Enter на пустой строке.\n'
              'Обратите внимание, что данный метод удалит ранее записанные сообщения!')

        messages = []
        while True:
            message = input('> ')
            if not message:
                break
            messages.append(message)
        settings.settings.set_messages(messages)
    else:
        settings.settings.set_messages(arg_messages.split('; '))

    print('Сообщения успешно добавлены!')


def monitor_kills() -> None:
    """Основной цикл мониторинга убийств."""
    try:
        cooldown_time = 8.5
        last_trigger_time = time.time() - cooldown_time

        with Vision() as vision:
            while True:
                current_time = time.time()

                if vision.detect_kill():
                    if current_time - last_trigger_time >= cooldown_time:
                        message = random.choice(settings.settings.messages)
                        say_quip(message)
                        last_trigger_time = current_time
                        keyboard.send('p')

                        if settings.settings.debug and settings.settings.save_frame:
                            vision.save_frame(message)

                if settings.settings.debug and settings.settings.screenrecord:
                    vision.screenrecord()

                if settings.settings.debug and settings.settings.print_fps:
                    vision.print_fps()

    except KeyboardInterrupt:
        sys.exit()


def process_arguments(args) -> None:
    """Обработка аргументов командной строки и взаимодействие с пользователем при необходимости."""

    if args.select_area:
        select_area()

    elif args.find_color:
        try:
            find_and_save_color()
        except AttributeError:
            print(
                'Инструмент не может работать, так как не обозначена рабочая область!\n'
                'Чтобы настроить её, вы можете запустить программу с флагом -sa или --select-area.\n'
                'Подробнее о команде можно узнать, запустив программу с флагом -h.'
            )

    elif args.path:
        set_game_path(args.path)

    elif args.messages:
        set_messages(args.messages)

    else:
        try:
            say_quip('')
            monitor_kills()
        except AttributeError:
            print(
                'Перед использованием, пожалуйста, настройте программу!\n'
                'Вы можете настроить вручную через файл "settings.cfg" или при помощи параметров, \n'
                'список которых можно получить, запустив программу с флагом -h.'
            )

        except FileNotFoundError:
            print(
                'Программа не может сгенерировать файлы конфигурации для игры CS2, так как не указан путь!\n'
                'Чтобы настроить путь, вы можете запустить программу с флагом -p или --path.\n'
                'Подробнее о команде можно узнать, запустив программу с флагом -h.'
            )


@settings.logger.catch()
def main() -> None:
    parser = argparse.ArgumentParser(
        prog='KillQuip',
        description='Программа для вывода в чат сообщения после совершенного убийства'
    )

    parser.add_argument('-sa', '--select-area', action='store_true', help='Выделить область для фиксации убийств')
    parser.add_argument('-fc', '--find-color', action='store_true', help='Инструмент для получения HSV нужного цвета')
    parser.add_argument('-p', '--path', nargs='?', const=True, help='Установить путь к корневой директории игры CS2')
    parser.add_argument('-m', '--messages', nargs='?', const=True,
                        help='Добавить сообщения для игры. Пример: "пиу", "пау", "хаха", "это было сложно",')

    args = parser.parse_args()

    process_arguments(args)


if __name__ == '__main__':
    main()
