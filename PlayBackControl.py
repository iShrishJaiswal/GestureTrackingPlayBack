import cv2
import HandTrackingModule as htm
import pyautogui as gui
import time

cap = cv2.VideoCapture(0)
detector = htm.HandDetector(detect_con=0.7, track_con=0.7)


def if_finger_stretch(lst, finger):
    decider = abs((lst[0][2] - lst[9][2]) / 2)
    index_finger = lst[5][2] - lst[8][2] > decider
    middle_finger = lst[9][2] - lst[12][2] > decider
    ring_finger = lst[13][2] - lst[16][2] > decider
    pinky_finger = lst[17][2] - lst[20][2] > decider
    thumb = abs(lst[5][1] - lst[4][1]) > decider
    if finger == 'index and thumb':
        return index_finger and thumb
    elif finger == 'all':
        return index_finger and middle_finger and ring_finger and pinky_finger and thumb
    elif finger == 'thumb':
        return thumb


def finger_direction(lst):
    if if_finger_stretch(lst, 'all'):
        return 'all'
    elif if_finger_stretch(lst, 'index and thumb'):
        if lst[8][1] < lst[4][1]:
            return 'forward'
        elif lst[8][1] > lst[4][1]:
            return 'backward'
    elif if_finger_stretch(lst, 'thumb'):
        tdir = lst[1][2] - lst[4][2]
        if tdir > 0:
            return 'up'
        elif tdir < 0:
            return 'down'


start_init = False
prev = -1
while True:
    end_time = time.time()
    _, img = cap.read()
    img = detector.find_hands(img)
    img = cv2.flip(img, 1)
    lm_list = detector.find_position(img, draw=False)
    if len(lm_list) != 0:
        fd = finger_direction(lm_list)
        print(fd)
        if prev != fd:
            if not start_init:
                start_time = time.time()
                start_init = True
            elif end_time - start_time > 0.2:
                if fd == 'forward':
                    gui.press('right')
                elif fd == 'backward':
                    gui.press('left')
                elif fd == 'up':
                    gui.press('up')
                elif fd == 'down':
                    gui.press('down')
                elif fd == 'all':
                    gui.press('space')
                prev = fd
                start_init = False
    cv2.imshow("Window", img)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break
