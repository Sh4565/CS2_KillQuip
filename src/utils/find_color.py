
import cv2
import mss
import numpy
import keyboard


def find_color(monitor: dict, hsv_min: tuple = (0, 0, 0), hsv_max: tuple = (255, 255, 255)) -> [tuple, tuple]:
    cv2.namedWindow("result")
    cv2.namedWindow("settings")

    cv2.createTrackbar('h1', 'settings', hsv_min[0], 255, lambda _: None)
    cv2.createTrackbar('s1', 'settings', hsv_min[1], 255, lambda _: None)
    cv2.createTrackbar('v1', 'settings', hsv_min[2], 255, lambda _: None)

    cv2.createTrackbar('h2', 'settings', hsv_max[0], 255, lambda _: None)
    cv2.createTrackbar('s2', 'settings', hsv_max[1], 255, lambda _: None)
    cv2.createTrackbar('v2', 'settings', hsv_max[2], 255, lambda _: None)

    sct = mss.mss()
    while True:
        img = numpy.asarray(sct.grab(monitor))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        h1 = cv2.getTrackbarPos('h1', 'settings')
        s1 = cv2.getTrackbarPos('s1', 'settings')
        v1 = cv2.getTrackbarPos('v1', 'settings')

        h2 = cv2.getTrackbarPos('h2', 'settings')
        s2 = cv2.getTrackbarPos('s2', 'settings')
        v2 = cv2.getTrackbarPos('v2', 'settings')

        h_min = numpy.array((h1, s1, v1), numpy.uint8)
        h_max = numpy.array((h2, s2, v2), numpy.uint8)

        thresh = cv2.inRange(hsv, h_min, h_max)

        cv2.imshow('result', thresh)

        cv2.waitKey(5)
        if keyboard.is_pressed('enter'):
            cv2.destroyAllWindows()
            return (h1, s1, v1), (h2, s2, v2)

        elif keyboard.is_pressed('esc') or keyboard.is_pressed('q'):
            cv2.destroyAllWindows()
            return None, None


if __name__ == '__main__':
    mon = {
        'top': 0,
        'left': 0,
        'width': 1920,
        'height': 1080
    }

    find_color(mon)
