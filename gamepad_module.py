import Gamepad
import time

# Gamepad settings
gamepadType = Gamepad.PS3
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
        print("Module say: " + control)
        return(control)
    elif eventType == 'AXIS':
        # Joystick changed
        if control == joystickSpeed:
            # Speed control (inverted)
            speed = -value
            #return("Speed = " + speed)
        elif control == joystickSteering:
            # Steering control (not inverted)
            steering = value
            #return("Steering = " + steering)
        #print('%+.1f %% speed, %+.1f %% steering' % (speed * 100, steering * 100))  

class KeyboardHelper:
  
    def __init__(self):
        self.__key_code = -1
        self.__loop = True
        self.__callback = None
        self.eventType, self.control, self.value = gamepad.getNextEvent()
        key_code = return_control(self.eventType, self.control, self.value)
        #self.__original_settings = termios.tcgetattr(sys.stdin)

    @property
    def key_code(self):
        return self.__key_code

    @key_code.setter
    def key_code(self, value):
        self.__key_code = value

    def set_callback(self, callback):
        self.__callback = callback

    def get_key_continuous(self):
        """continuous_get_key records keystrokes in a while loop controlled by the private variable __loop.
        """
        while self.__loop:
            self.__get_key()

        #termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.__original_settings)

    def end_get_key_continuous(self):
        """end_loop sets the private variable __loop to false so that the while loop from continuous_get_key is stopped.
        """
        self.__loop = False

    def __get_key(self, return_control):
        #tty.setcbreak(sys.stdin)
        self.eventType, self.control, self.value = gamepad.getNextEvent()
        key_code = return_control(self.eventType, self.control, self.value)
        #termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.__original_settings)
        self.__callback(key_code)