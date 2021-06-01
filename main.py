''' 
This program makes it possible to send commands to a Tello drone through a webcamera. 
The program is created by: Controlled drone (S2126631-1) - 4. semester - spring 2021
'''
# Import the necessary modules
from interface import GUI

# The main function
def main():
    ''' Begins method startGUI() from class GUI() '''
    print("Starting GUI...")
    GUI.startGUI()

# Executes main if the file is run directly and not imported
if __name__ == "__main__":
    main()
