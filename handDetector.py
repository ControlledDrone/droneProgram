# Imports the necessary modules
import cv2
import mediapipe as mp


class HandDetector():
    ''' A class used to run graphical user interface with opencv
    ...
    Attributes
    ----------
    img :
    draw :
    handNo :
    
    Methods
    -------
    findHands(self, img, draw=True):
        Method finds hands in img and return img with hands drawn
    findPosition(self, img, handNo=0, draw=True):
        Method used to return list of landmarks in img
    '''

    # Constructor for hand detector
    def __init__(self, mode=False, maxHands=1, detectionCon=0.7, trackCon=0.6):
        '''
        Method for handling left mouse click event
        ...
        Parameters
        ----------
            mode :
            maxHands :
            detectionCon :
            trackCon :
        '''
        self.mode = mode
        self.maxHands = maxHands  # Set to 1 to minimize confusion between detected hands
        self.detectionCon = detectionCon  # Optimal between 0.5-0.8
        self.trackCon = trackCon  # Optimal between 0.5-0.8

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    # Method finds hands in img and return img with hands drawn
    def findHands(self, img, draw=True):
        '''
        Method to find hands in img and return img with hands drawn
        ...
        Parameters
        ----------
        img :
        draw :
        
        Returns
        -------
        img
        '''
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    # Method used to return list of landmarks in img
    def findPosition(self, img, handNo=0, draw=True):
        '''
        Method for handling left mouse click event
        ...
        Parameters
        ----------
        img : 
        handNo :
        draw :
        
        Returns
        -------
        lmList
        '''
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 4, (255, 205, 195), cv2.FILLED)  # Silver color
        return lmList
