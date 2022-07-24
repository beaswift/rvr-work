#import sys
#import termios
#import tty
import Gamepad
import time

gamepadType = Gamepad.PS3

joystickSpeed = 'LEFT-Y'
joystickSteering = 'RIGHT-X'

speed = 0.0
steering = 0.0

if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = gamepadType()
print('Gamepad connected')

class Ps3Helper:

    def __init__(self):
        self.__control = -1
        self.__loop = True
        self.__callback = None
        #self.__control = self.get_gamepad_input()

    def get_gamepad_input(self):
        eventType, control, value = gamepad.getNextEvent()
        
        if value:
            
            if eventType == 'BUTTON':
                # Button changed
                #print(control)
                self.__callback(control)
                #return(control)   
            #elif eventType == 'AXIS':
                # Joystick changed
            #    if control == joystickSpeed:
            #        # Speed control (inverted)
            #        speed = -value
            #        return("Speed = " + speed)
            #    elif control == joystickSteering:
            #        # Steering control (not inverted)
            #        steering = value
            #        return("Steering = " + steering)
            #    #print('%+.1f %% speed, %+.1f %% steering' % (speed * 100, steering * 100))
                #self.__callback(control)

    @property
    def control(self):
        return self.__control

    @control.setter
    def control(self, value):
        self.__control = value

    def set_callback(self, callback):
        self.__callback = callback

    def get_control_continuous(self):
        """continuous_get_key records keystrokes in a while loop controlled by the private variable __loop.

        """
        while self.__loop:
            self.get_gamepad_input()

        #termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.__original_settings)

    def end_get_control_continuous(self):
        """end_loop sets the private variable __loop to false so that the while loop from continuous_get_key is stopped.

        """
        self.__loop = False

#    def __get_key(self):
#        tty.setcbreak(sys.stdin)
#        key_code = ord(sys.stdin.read(1))
#        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.__original_settings)
#        self.__callback(key_code)
