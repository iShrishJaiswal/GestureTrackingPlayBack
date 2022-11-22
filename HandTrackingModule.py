import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, mode=False, max_hands=2, complexity=1, detect_con=0.5, track_con=0.5):
        self.results = None
        self.mode = mode
        self.maxHands = max_hands
        self.complexity = complexity
        self.detectCon = detect_con
        self.trackCon = track_con

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS)

        return img

    def find_position(self, img, hand_no=0, draw=True):

        lm_list = []

        if self.results.multi_hand_landmarks:
            if len(self.results.multi_hand_landmarks) >= hand_no + 1:
                cur_hand = self.results.multi_hand_landmarks[hand_no]
                for hlmId, lm in enumerate(cur_hand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lm_list.append([hlmId, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lm_list
