# Import the necessary modules
from handDetector import HandDetector
from droneControls import DroneControls
from navigateDrone import NavigateDrone
from dji

py import tello
import cv2
import time

# Connects to Tello drone
me = tello.Tello()
me.connect()

knowInstructions = False


class GUI():
    ''' A class used to run graphical user interface with opencv
    ...

    Attributes
    ----------


    Methods
    -------
    ifClicked(event, x, y, flags, params):
        Method for handling left mouse click event
    instructions(DroneGUI):
        Method for showing instructions in opencv
    insideRectangle(img, x, y):
        Method for checking if point is inside rectangles
    printDirection(img, vals, noOfFingers):
                                                        !!!MANGLER METODE FORKLARING!!!
    startGUI():
                                                        !!!MANGLER METODE FORKLARING!!!
    '''
    def ifClicked(event, x, y, flags, params):
        '''
        Method for handling left mouse click event

        Parameters
        ----------

        Returns
        -------
        None
        '''
        
        global knowInstructions
        if event == cv2.EVENT_LBUTTONDOWN:
            knowInstructions = not knowInstructions

    def instructions(DroneGUI):
        '''
        Method for showing instructions in opencv

        Parameters
        ----------

        Returns
        -------
        None
        '''
        # Put text header
        cv2.putText(DroneGUI, "Instructions", (187, 55), cv2.FONT_HERSHEY_TRIPLEX,
                    2, (255, 255, 255), 1)
        cv2.line(DroneGUI, (175, 72), (620, 72), (255, 255, 255), 2)
        # Instructions text for controlling the drone
        cv2.rectangle(DroneGUI, (15, 90), (785, 510), (160, 160, 160), 1)
        cv2.putText(DroneGUI, "How to control the drone:", (30, 120), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    1, (255, 255, 255), 1)
        cv2.putText(DroneGUI, "You must use your left hand", (31, 142), cv2.FONT_HERSHEY_PLAIN,
                    1, (255, 255, 255), 1)
        # How to navigate the drone
        cv2.circle(DroneGUI, (40, 180), 5, (255, 255, 255), cv2.FILLED)
        cv2.circle(DroneGUI, (40, 238), 5, (255, 255, 255), cv2.FILLED)
        cv2.circle(DroneGUI, (40, 296), 5, (255, 255, 255), cv2.FILLED)
        cv2.circle(DroneGUI, (40, 354), 5, (255, 255, 255), cv2.FILLED)
        cv2.circle(DroneGUI, (40, 412), 5, (255, 255, 255), cv2.FILLED)
        cv2.circle(DroneGUI, (40, 470), 5, (255, 255, 255), cv2.FILLED)
        cv2.putText(DroneGUI, "Close hand to rotate clockwise", (65, 187), cv2.FONT_HERSHEY_PLAIN,
                    1, (255, 255, 255), 1)
        cv2.putText(DroneGUI, "To hower hold up pointerfinger", (65, 245), cv2.FONT_HERSHEY_PLAIN,
                    1, (255, 255, 255), 1)
        cv2.putText(DroneGUI, "Move pointerfinger into rectangles to takeoff and land", (65, 303),
                    cv2.FONT_HERSHEY_PLAIN,
                    1, (255, 255, 255), 1)
        cv2.putText(DroneGUI, "Show pointer- and middlefinger to move up and down", (65, 361), cv2.FONT_HERSHEY_PLAIN,
                    1, (255, 255, 255), 1)
        cv2.putText(DroneGUI, "Show pointer-, middle- and ringfinger to move left and right", (65, 419),
                    cv2.FONT_HERSHEY_PLAIN,
                    1, (255, 255, 255), 1)
        cv2.putText(DroneGUI, "Show openhand to move forwards and backwards", (65, 477), cv2.FONT_HERSHEY_PLAIN,
                    1, (255, 255, 255), 1)
        # Getting images showing hand gestures and resizing them
        closedHandImg = cv2.imread(r'.venv\00.jpg')
        closedHandImg = cv2.resize(closedHandImg, (75, 100))
        oneFingerImg = cv2.imread(r'.venv\01.jpg')
        oneFingerImg = cv2.resize(oneFingerImg, (75, 100))
        twoFingersImg = cv2.imread(r'.venv\02.jpg')
        twoFingersImg = cv2.resize(twoFingersImg, (75, 100))
        threeFingersImg = cv2.imread(r'.venv\03.jpg')
        threeFingersImg = cv2.resize(threeFingersImg, (75, 100))
        openHandImg = cv2.imread(r'.venv\05.jpg')
        openHandImg = cv2.resize(openHandImg, (75, 100))
        # Defining where to put the images on an image
        DroneGUI[95:195, 700:775] = closedHandImg
        DroneGUI[170:270, 620:695] = oneFingerImg
        DroneGUI[250:350, 700:775] = twoFingersImg
        DroneGUI[330:430, 620:695] = threeFingersImg
        DroneGUI[405:505, 700:775] = openHandImg

        # Putting text indicating how to start controlling the drone
        cv2.putText(DroneGUI, "Start", (350, 550), cv2.FONT_HERSHEY_TRIPLEX,
                    1, (0, 255, 0), 1)
        cv2.putText(DroneGUI, "by clicking the mouse", (250, 580), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    1, (255, 255, 255), 1)

        # Display instructions on image in the specified window (DroneGUI)
        cv2.imshow('DroneGUI', DroneGUI)

    def insideRectangle(img, x, y):
        '''
        Method for checking if point is inside rectangles

        Parameters
        ----------

        Returns
        -------
        None
        '''
        # Rectangles in GUI for takeoff and landing
        cv2.rectangle(img, (478, 0), (593, 30), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, "Landing", (488, 21), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (255, 255, 255), 1)
        cv2.line(img, (594, 0), (594, 30), (255, 255, 255), 1)
        cv2.rectangle(img, (595, 0), (710, 30), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, "Takeoff", (606, 21), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (255, 255, 255), 1)

        # Detecting whether cordinate is inside rectangles in opencv
        if x > 478 and x < 593 and y > 0 and y < 30:  # Landing
            cv2.rectangle(img, (0, 0), (470, 30), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, "Drone is landing...", (15, 21), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1, (0, 0, 0), 1)
            me.land()
        elif x > 595 and x < 710 and y > 0 and y < 30:  # Take off
            cv2.rectangle(img, (0, 0), (470, 30), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, "Drone takeoff...", (15, 21), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1, (0, 0, 0), 1)
            me.takeoff()

    def printDirection(img, vals, noOfFingers):
        '''
        Method for XXX

        Parameters
        ----------

        Returns
        -------
        None
        '''
        cv2.rectangle(img, (0, 0), (800, 30), (255, 255, 255), cv2.FILLED)
        # Displaying text for certain fingercounts
        if noOfFingers == 0:
            cv2.putText(img, "Rotating counter clockwise...", (15, 21),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
        elif noOfFingers == 1:
            cv2.putText(img, "Hovering...", (15, 21),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
        # Displaying text for certain fingercounts and values
        elif noOfFingers == 2 and vals[2] != 0:
            if vals[2] < 0:
                cv2.putText(img, "Flying down with speed " + str(int(vals[2] * -1)) + "...", (15, 21),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
            elif vals[2] > 0:
                cv2.putText(img, "Flying up with speed " + str(int(vals[2])) + "...", (15, 21),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
        elif noOfFingers == 3 and vals[0] != 0:
            if vals[0] < 0:
                cv2.putText(img, "Flying left with speed " + str(int(vals[0] * -1)) + "...", (15, 21),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
            elif vals[0] > 0:
                cv2.putText(img, "Flying right with speed " + str(int(vals[0])) + "...", (15, 21),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
        elif noOfFingers == 5 and vals[1] != 0:
            if vals[1] < 0:
                cv2.putText(img, "Flying backwards with speed " + str(int(vals[1] * -1)) + "...", (15, 21),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)
            elif vals[1] > 0:
                cv2.putText(img, "Flying forwards with speed " + str(int(vals[1])) + "...", (15, 21),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), 1)

    def startGUI():
        '''
        Method for XXX

        Parameters
        ----------

        Returns
        -------
        None
        '''
        # Class objects
        detector = HandDetector()
        drone = DroneControls()
        navDrone = NavigateDrone()

        # Variables used for calculating frames per second (fps) and setting the frame size for webcam
        pTime = 0
        cTime = 0
        frameWidth = 800
        frameHeight = 600

        # Capture video from webcam
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # Set width and height for webcam
        cap.set(3, frameWidth)
        cap.set(4, frameHeight)
        cap.set(10, 70)  # Set brightness for webcam

        # Set GUI window
        img = cv2.namedWindow('DroneGUI')
        cv2.setMouseCallback('DroneGUI', GUI.ifClicked)

        # Getting image used as background for instructions
        background = cv2.imread(r'.venv\background.jpg')
        DroneGUI = cv2.resize(background, (frameWidth, frameHeight))

        # Getting the battery power
        battery_status = drone.tello_battery(me)

        while True:
            # Read webcamera input and print text if error
            success, img = cap.read()
            if not success:
                print("Unable to capture webcamera...")

            # Shows instructions for program - If left mouse is clicked
            if (knowInstructions == False):
                # Call method to show instructions in opencv
                GUI.instructions(DroneGUI)

            # Shows webcam view
            else:
                # Flips img horizontally to create a mirror effect
                img = cv2.flip(img, 1)
                # Finds hands and landmarks in the webcamera img
                img = detector.findHands(img)
                lmList = detector.findPosition(img)
                # List of fingertips for finding open fingers
                tipIds = [4, 8, 12, 16, 20]
                # Design of GUI
                cv2.putText(img, "Show hand to control drone", (146, 29),
                            cv2.FONT_HERSHEY_TRIPLEX, 1, (10, 255, 90), 1)  # Green color
                # Checks if there are any landmarks in the img
                if len(lmList) != 0:
                    # Finds coordinates for center of hand
                    centerCoordinateHand = drone.findMiddleXYOfLms(lmList[9], lmList[0])
                    # Draws and finds line for velocity
                    center_dist = drone.findVeloFromCenter(img, centerCoordinateHand)
                    # Creates deadzone that activates when center coordinate is inside
                    drone.createDeadZone(img, centerCoordinateHand)

                    # Getting x and y coordinates of landmarks 0, 8 and 9
                    x0, y0 = drone.findXYofLm(lmList[0])
                    x8, y8 = drone.findXYofLm(lmList[8])
                    x9, y9 = drone.findXYofLm(lmList[9])
                    # Draws line used for depth
                    cv2.line(img, (x9, y9), (x0, y0), (190, 170, 160), 3)  # Gray color
                    # Finds distance between two landmarks
                    distance1 = drone.findDistanceLms(lmList[9], lmList[0])
                    # Finds number of fingers
                    noOfFingers = drone.findNoOfFingers(img, lmList, tipIds)

                    # If left hand is closed
                    if noOfFingers == 0:
                        me.rotate_counter_clockwise(9)  # Rotate drone
                    # If left pointer finger are up then drone hovers
                    if noOfFingers == 1:
                        me.stop()
                        print("HOVERING")

                    # Navigate the drone
                    vals = navDrone.navigateDrone(centerCoordinateHand, img, noOfFingers, center_dist, distance1)
                    # Needed to senc rc controls to Tello drone
                    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
                    # Prints direction drone is flying in opencv
                    GUI.printDirection(img, vals, noOfFingers)
                    # Checks if certain coordinates are within certain rectangles for take off and landing
                    GUI.insideRectangle(img, x8, y8)
                    # For GUI design only
                    cv2.rectangle(img, (0, 0), (800, 30), (150, 150, 150), 1)
                    cv2.putText(img, "Mouse click for instructions", (430, 590),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 1)  # Gray color

                # Calculates fps
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                # Add text with fps to opencv (Changes color from green to red color indicating good or bad)
                if fps > 0 and fps < 15:
                    cv2.putText(img, "FPS:" + str(int(fps)), (716, 21), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                (0, 0, 255), 1)
                elif fps > 15:
                    cv2.putText(img, "FPS:" + str(int(fps)), (716, 21), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                                (0, 255, 0), 1)

                # Add text with drones battery level to opencv
                cv2.putText(img, "Battery: {}".format(battery_status) + "%", (10, 590),
                            cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (140, 140, 140), 1)  # Gray color

                cv2.imshow('DroneGUI', img)

                i = cv2.waitKey(1)
                # Safety for drone landing on key 'l'
                if i & 0xFF == ord('l'):
                    print("landing")
                    me.land()
                    break

            o = cv2.waitKey(1)
            # Close program on key 'q'
            if o & 0xFF == ord('q'):
                print("Closing")
                break

        # End drone connection, release webcamera and close all opencv windows
        me.end()
        cap.release()
        cv2.destroyAllWindows()
