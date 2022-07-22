# Load the gamepad and time libraries
import Gamepad
import time

# Gamepad settings
gamepadType = Gamepad.PS3
buttonX = 'CROSS'
buttonO = 'CIRCLE'
buttonExit = 'PS'
buttonForward = 'DPAD-UP'
buttonBackward = 'DPAD-DOWN'
buttonLeft = 'DPAD-LEFT'
buttonRight = 'DPAD-RIGHT'
joystickSpeed = 'LEFT-Y'
joystickSteering = 'RIGHT-X'

# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = gamepadType()
print('Gamepad connected')

# Set some initial state
speed = 0.0
steering = 0.0

def return_control(eventType, control, value):
    if eventType == 'BUTTON':
        # Button changed
        print(control)
        return(control)
    elif eventType == 'AXIS':
        # Joystick changed
        if control == joystickSpeed:
            # Speed control (inverted)
            speed = -value
            return("Speed = " + speed)
        elif control == joystickSteering:
            # Steering control (not inverted)
            steering = value
            return("Steering = " + steering)
        #print('%+.1f %% speed, %+.1f %% steering' % (speed * 100, steering * 100))

# Handle joystick updates one at a time
while gamepad.isConnected():
    # Wait for the next event
    eventType, control, value = gamepad.getNextEvent()
    if value:
        return_control(eventType, control, value)

