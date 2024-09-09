
import cv2
import mss
import time
import numpy
import keyboard
import settings

from pathlib import Path
from settings import logger
from data.models import KillHSV, BoundingBox


class Vision:
    def __init__(self):
        self.fps = 0
        self.img = None
        self.sct = mss.mss()
        self.file_number = 0
        self.start_time_fps = time.time()

    def print_fps(self) -> None:
        """Выводит количество кадров в секунду (FPS) в консоль."""
        current_time = time.time()
        if current_time - self.start_time_fps >= 1:
            print(f'FPS: {self.fps}', end='\r')
            self.fps = 0
            self.start_time_fps = current_time

    def screenrecord(self) -> bool:
        """Отображает изображение на экране и проверяет, нажата ли клавиша 'Esc' для выхода."""
        cv2.imshow('Tactical map', self.img)
        cv2.waitKey(25)
        if keyboard.is_pressed('esc'):
            cv2.destroyAllWindows()
            return False
        return True

    def detect_kill(self) -> bool:
        """Обрабатывает изображение для определения событий убийства на экране."""
        start_time = time.time()
        self.img = numpy.asarray(self.sct.grab(BoundingBox.get_dict))

        h_min = numpy.array(KillHSV.min, numpy.uint8)
        h_max = numpy.array(KillHSV.max, numpy.uint8)

        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, h_min, h_max)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            contour_area = cv2.contourArea(contour)
            if contour_area < 1000:
                continue

            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4 and self._is_rectangle(approx):
                cv2.drawContours(self.img, [approx], 0, (0, 255, 0), 2)
                self.fps += 1
                self.limit_fps(start_time)
                return True

        self.fps += 1
        self.limit_fps(start_time)
        return False

    def save_frame(self, message: str):
        """Сохраняет текущее изображение в указанный файл."""
        data_path = Path(settings.BASE_DIR, 'data')
        data_path.mkdir(exist_ok=True)
        file_number = len(list(data_path.glob('*.jpg'))) + 1
        path_file = data_path / f'detect_{file_number}.jpg'

        cv2.imwrite(str(path_file), self.img)
        logger.debug(f'Сообщение №{file_number}; Текст: "{message}"; Файл: "{path_file}"')

    @staticmethod
    def _is_rectangle(approx) -> bool:
        """Проверяет, является ли контур прямоугольником с углами около 90 градусов."""
        def angle_cosine(p_0, p_1, p_2):
            """Вычисляет косинус угла между векторами p0p1 и p1p2."""
            d1, d2 = p_0 - p_1, p_2 - p_1
            return numpy.dot(d1, d2) / (numpy.linalg.norm(d1) * numpy.linalg.norm(d2))

        angles = []
        for i in range(4):
            p0 = approx[i][0]
            p1 = approx[(i + 1) % 4][0]
            p2 = approx[(i + 2) % 4][0]
            cosine = angle_cosine(numpy.array(p0), numpy.array(p1), numpy.array(p2))
            angles.append(cosine)

        # Проверяем, что все углы близки к 90 градусам (косинус угла близок к 0)
        return all(abs(angle) < 0.3 for angle in angles)

    @staticmethod
    def limit_fps(start_time):
        """Ограничивает частоту обработки кадров"""
        if settings.settings.fps_max:
            frame_time = 1.0 / settings.settings.fps_max
            elapsed_time = time.time() - start_time
            if elapsed_time < frame_time:
                time.sleep(frame_time - elapsed_time)

    def __enter__(self):
        """Инициализация при входе в контекстный менеджер."""
        self.start_time_fps = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Завершение работы и очистка ресурсов."""
        self.sct = None
        cv2.destroyAllWindows()
