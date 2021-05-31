# Import the necessary modules
import cv2
import math
import numpy as np


# Class used to make calculations to control and get info on drone
class DroneControls():
    # Method to get the value of drone's battery power
    def tello_battery(self, me):
        global battery_status
        battery_status = me.get_battery()
        return int(battery_status)

    # Method creates deadzone in the center of the img when a certain landmark is inside
    def createDeadZone(self, img, lmPos):
        x, y = lmPos[0:]
        h, w = img.shape[:2]
        screen_center_w = w / 2
        screen_center_h = h / 2

        dead_zone_size = 100
        out_of_dz = True

        # If landmark is inside deadzone return out_of_dz == false
        if x < screen_center_w + dead_zone_size and x > screen_center_w - dead_zone_size and y < screen_center_h + dead_zone_size and y > screen_center_h + dead_zone_size:
            return out_of_dz == False

    # Method used to find the velocity from the center of the img to a certain landmark
    def findVeloFromCenter(self, img, lmPos):
        x, y = lmPos[0:]
        h, w = img.shape[:2]
        # Calculating the distance from center to coordinates
        center_dist = np.linalg.norm(np.array((x, y)) - np.array((h / 2, w / 2)))
        # Draws velocity line in opencv with function line
        cv2.line(img, (x, y), (int(w / 2), int(h / 2)), (30, 30, 30), 1)  # Black color
        # Draws lines to form a cross in center of screen
        cv2.line(img, (int(w / 2), int(h / 2)), (int(w / 2) + 7, int(h / 2)), (255, 255, 255), 1)
        cv2.line(img, (int(w / 2), int(h / 2)), (int(w / 2), int(h / 2) + 7), (255, 255, 255), 1)
        cv2.line(img, (int(w / 2), int(h / 2)), (int(w / 2) - 7, int(h / 2)), (255, 255, 255), 1)
        cv2.line(img, (int(w / 2), int(h / 2)), (int(w / 2), int(h / 2) - 7), (255, 255, 255), 1)
        return int(center_dist)

    # Method used to find the distance between two landmarks
    def findDistanceLms(self, lmPos1, lmPos2):
        x1, y1 = lmPos1[1:]
        x2, y2 = lmPos2[1:]
        # Calculates distance (line: 52) learned from the website: https://morioh.com/p/9ce670a59fc3
        distance = math.hypot(x2 - x1, y2 - y1)
        return distance

    # Method used to find the middle coordinate between two landmarks
    def findMiddleXYOfLms(self, lmPos1, lmPos2):
        x1, y1 = lmPos1[1:]
        x2, y2 = lmPos2[1:]
        # Calculates the middle coordinate between the two landmarks
        x, y = (x1 + x2) // 2, (y1 + y2) // 2
        return x, y

    # Method used to return the x and y values for a certain landmark
    def findXYofLm(self, lmPos1):
        x, y = lmPos1[1:]
        return x, y

    # Method returns height and width of our webcamera img    
    def findScreenCenter(img):
        h, w = img.shape[:2]
        screen_center_h = h / 2
        screen_center_w = w / 2
        return screen_center_h, screen_center_w

    # Method used to find and return open fingers 
    def findNoOfFingers(self, img, lmList, tipIds):
        # Creates a list for finding and storing open fingers
        fingers = []
        # If there are landmarks in the webcamera image
        if len(lmList) != 0 in img:
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Loop for fingers minus thumb
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            # Returns number of fingers to variable noOfFingers
            noOfFingers = fingers.count(1)
            print(noOfFingers)

        return noOfFingers
