
import sys
import cv2
import time
import mouse
import keyboard


def area_selection():
    while True:
        if keyboard.is_pressed('shift') and keyboard.is_pressed('win') and keyboard.is_pressed('s'):
            break
        elif keyboard.is_pressed('q') or keyboard.is_pressed('esc'):
            sys.exit()

    press_time = None
    mouse_pressed = False
    left, top = None, None

    while True:
        if keyboard.is_pressed('q') or keyboard.is_pressed('esc'):
            cv2.destroyAllWindows()
            return None

        if mouse.is_pressed('left'):
            if not mouse_pressed:
                mouse_pressed = True
                press_time = time.time()
                left, top = mouse.get_position()

        if not mouse.is_pressed('left') and mouse_pressed:
            mouse_pressed = False
            release_time = time.time()
            right, bottom = mouse.get_position()
            hold_duration = release_time - press_time
            if hold_duration >= 1 and left and top:
                return top, left, right - left, bottom - top


if __name__ == '__main__':
    top1, left1, width1, height1 = area_selection()
    print(top1, left1, width1, height1)
