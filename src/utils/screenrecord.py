
import cv2
import keyboard


def screenrecord(img: cv2):
    cv2.imshow('Tactical map', img)
    cv2.waitKey(25)

    if keyboard.is_pressed('esc'):
        cv2.destroyAllWindows()
        return False
    else:
        return True
