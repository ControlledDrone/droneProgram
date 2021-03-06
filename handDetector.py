# Imports the necessary modules
import cv2
import mediapipe as mp


class HandDetector():
    ''' A class used to run graphical user interface with opencv '''

    
    def __init__(self, mode=False, maxHands=1, detectionCon=0.7, trackCon=0.6):
        '''  Constructor for hand detector '''
        self.mode = mode
        self.maxHands = maxHands  # Set to 1 to minimize confusion between detected hands
        self.detectionCon = detectionCon  # Optimal between 0.5-0.8
        self.trackCon = trackCon  # Optimal between 0.5-0.8

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        ''' Method to find hands in img and return img with hands drawn '''
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        # If there's hands with landmarks in the image
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                # Draw landmarks and connections between on imag
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        ''' Method to return list of landmarks in img '''
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy]) # Get id,x- and y coordinate of landmark
                if draw:
                    cv2.circle(img, (cx, cy), 4, (255, 205, 195), cv2.FILLED)  # Silver color
        return lmList
