# Import the necessary modules
from droneControls import DroneControls


class NavigateDrone():
    ''' A class used to make drone fly in choosen directions '''

    def navigateDrone(self, centercoordinate, img, noOfFingers, center_dist, distance1):
        ''' Method used for navigating drone left, right, forwards, backwards, up, dawn, yaw'''
        # Find center height and width of given img 
        screen_center_h, screen_center_w = DroneControls.findScreenCenter(img)

        lr, fb, ud, yv = 0, 0, 0, 0  # LeftRight, ForwardBackward, UpDown, Yaw (side to side)
        speed = 10

        # If pointer finger and middle finger are up and..
        if noOfFingers == 2 and centercoordinate[1] < screen_center_h:
            ud = int(center_dist / 10)
        elif noOfFingers == 2 and centercoordinate[1] > screen_center_h:
            ud = int((-center_dist / 10) * 2)

        # If pointer finger, middle finger and ring finger are up and..
        if noOfFingers == 3 and centercoordinate[0] > screen_center_w:
            lr = int(5 + (center_dist / 10))
        elif noOfFingers == 3 and centercoordinate[0] < screen_center_w:
            lr = int((-center_dist / 10) * 2)

        # Backwards command if all four fingers are up but not the thumb and..
        if noOfFingers == 5:
            if distance1 < 140 and distance1 > 110:
                fb = -speed - 10
            elif distance1 < 110 and distance1 > 80:
                fb = -speed - 20
            elif distance1 < 80 and distance1 > 50:
                fb = -speed - 30
        # Forward command if all four fingers are up but not the thumb and..
        if noOfFingers == 5:
            if distance1 > 160 and distance1 < 190:
                fb = speed + 10
            elif distance1 > 190 and distance1 < 220:
                fb = speed + 20
            elif distance1 > 220 and distance1 < 250:
                fb = speed + 30

        # Return values for LeftRight, ForwardBackward, UpDown, Yaw (side to side)
        return lr, fb, ud, yv
