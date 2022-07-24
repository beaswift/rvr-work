import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import asyncio

import Gamepad
import time

#from gamepad_module import KeyboardHelper
from sphero_sdk import SerialAsyncDal
from sphero_sdk import SpheroRvrAsync

# initialize global variables
#key_helper = KeyboardHelper()
current_key_code = -1
driving_keys = [119, 97, 115, 100, 32]
speed = 0
heading = 0
flags = 0


# Gamepad settings
gamepadType = Gamepad.PS3
gamepad = gamepadType()
joystickSpeed = 'LEFT-Y'
joystickSteering = 'RIGHT-X'

def return_control(eventType, control, value):
    if eventType == 'BUTTON':
        # Button changed
        current_key_code = control
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



loop = asyncio.get_event_loop()
rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

def keycode_callback(keycode):
    global current_key_code
    current_key_code = keycode
    print("Key code updated: ", str(current_key_code))


async def main():
    """
    Runs the main control loop for this demo.  Uses the KeyboardHelper class to read a keypress from the terminal.
    W - Go forward.  Press multiple times to increase speed.
    A - Decrease heading by -10 degrees with each key press.
    S - Go reverse. Press multiple times to increase speed.
    D - Increase heading by +10 degrees with each key press.
    Spacebar - Reset speed and flags to 0. RVR will coast to a stop
    """
    global current_key_code
    global speed
    global heading
    global flags

    await rvr.wake()

    await rvr.reset_yaw()

    while True:
        print(current_key_code)

        if current_key_code == 'DPAD-UP':  # W
            # if previously going reverse, reset speed back to 64
            if flags == 1:
                speed = 64
            else:
                # else increase speed
                speed += 64
            # go forward
            flags = 0
        elif current_key_code == 'DPAD-DOWN':  # A
            heading -= 10
        elif current_key_code == 'DPAD-RIGHT':  # S
            # if previously going forward, reset speed back to 64
            if flags == 0:
                speed = 64
            else:
                # else increase speed
                speed += 64
            # go reverse
            flags = 1
        elif current_key_code == 'DPAD-RIGHT':  # D
            heading += 10
        elif current_key_code == 'CROSS':  # SPACE
            # reset speed and flags, but don't modify heading.
            speed = 0
            flags = 0

        # check the speed value, and wrap as necessary.
        if speed > 255:
            speed = 255
        elif speed < -255:
            speed = -255

        # check the heading value, and wrap as necessary.
        if heading > 359:
            heading = heading - 359
        elif heading < 0:
            heading = 359 + heading

        # reset the key code every loop
        current_key_code = -1

        # issue the driving command
        await rvr.drive_with_heading(speed, heading, flags)

        # sleep the infinite loop for a 10th of a second to avoid flooding the serial port.
        await asyncio.sleep(0.1)


def run_loop():
    global loop
#    global key_helper
    while gamepad.isConnected():
        # Wait for the next event
        eventType, control, value = gamepad.getNextEvent()
        if value:
            return_control(eventType, control, value)
    return_control(eventType, control, value)
    #key_helper.set_callback(keycode_callback)
    loop.run_until_complete(
        asyncio.gather(
            main()
        )
    )


if __name__ == "__main__":
    #loop.run_in_executor(None, key_helper.get_key_continuous)
    try:
        run_loop()
    except KeyboardInterrupt:
        print("Keyboard Interrupt...")
    #    key_helper.end_get_key_continuous()
    finally:
        print("Press any key to exit.")
        exit(1)