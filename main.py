from os import environ
import math  # Import the math module
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import time
import vgamepad as vg  # Import the virtual gamepad library
import tkinter as tk  # Import the tkinter library for GUI

# Initialize the virtual gamepad
gamepad = vg.VDS4Gamepad()

# Create a Tkinter window
window = tk.Tk()
window.title("Sony PS4 Dualshock")  # Set window title

# Global Settings
center_x, center_y = window.winfo_screenwidth() // 2, window.winfo_screenheight() // 2  # Calculate screen center
deadzone = 0.1  # Deadzone for joystick
interp_factor = 0.5  # Interpolation factor for mouse movement
x_sensitivity = 1.0  # X-axis sensitivity
y_sensitivity = 1.0  # Y-axis sensitivity
curve_power = 2  # Power for custom curve

# Previous mouse position
prev_x, prev_y = window.winfo_screenwidth() // 2, window.winfo_screenheight() // 2  # Initialize previous mouse position

# Key-to-button mapping
key_to_button_mapping = {
    "q": vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT,  # Map 'q' key to left shoulder button
    "e": vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT,  # Map 'e' key to right shoulder button
    "x": [vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_LEFT, vg.DS4_BUTTONS.DS4_BUTTON_SHOULDER_RIGHT], # Map 'x' key to combo shoulder buttons
    "f": vg.DS4_BUTTONS.DS4_BUTTON_SQUARE,  # Map 'f' key to square button
    "r": vg.DS4_BUTTONS.DS4_BUTTON_SQUARE,  # Map 'r' key to square button
    " ": vg.DS4_BUTTONS.DS4_BUTTON_CROSS,  # Map spacebar key to cross button
    "1": vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE,  # Map '1' key to triangle button
    "2": vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE,  # Map '2' key to triangle button
    "3": vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE,  # Map '3' key to triangle button
    "g": vg.DS4_BUTTONS.DS4_BUTTON_TRIANGLE,  # Map 'g' key to triangle button
    "c": vg.DS4_BUTTONS.DS4_BUTTON_CIRCLE,  # Map 'c' key to circle button
    "v": vg.DS4_BUTTONS.DS4_BUTTON_THUMB_RIGHT,  # Map 'v' key to right thumbstick button
}

# Function to apply custom curve to value
def apply_curve(value):
    if value >= 0:
        return math.pow(value, curve_power)
    else:
        return -math.pow(-value, curve_power)

# Function to convert mouse movement to joystick movement for first analog
def mouse_to_joystick(x, y):
    global prev_x, prev_y

    # Interpolate between previous and current mouse positions with a higher factor
    x = prev_x + (x - prev_x) * interp_factor
    y = prev_y + (y - prev_y) * interp_factor

    x_offset = (x - center_x) * x_sensitivity
    y_offset = (y - center_y) * y_sensitivity  

    # Apply deadzone 
    if abs(x_offset) < deadzone * center_x:
        x_offset = 0.0 
    if abs(y_offset) < deadzone * center_y:
        y_offset = 0.0

    x_value = x_offset / center_x
    y_value = y_offset / center_y

    # Apply custom curve to x and y offsets
    x_value = apply_curve(x_value)
    y_value = apply_curve(y_value)

    # Update previous mouse position
    prev_x, prev_y = x, y

    # Emulate joystick movement for first analog
    emulate_right_analog_movement(x_value, y_value)

# Function to emulate joystick movement for first analog
def emulate_right_analog_movement(x, y):
    gamepad.right_joystick_float(x_value_float=x, y_value_float=y)
    gamepad.update()

scroll_button_pressed = False

def emulate_mouse_click(event=None):
    global scroll_button_pressed
    
    if event is None:
        return
    
    if event.num == 1:  # Left mouse button for aiming
        gamepad.left_trigger_float(value_float=0.5)  # Emulate pressing L2 button (left trigger)
        gamepad.update()
    elif event.num == 3:  # Right mouse button for shooting
        gamepad.right_trigger_float(value_float=1.0)  # Emulate pressing R2 button (right trigger)
        gamepad.update()
    elif event.num == 2 and not scroll_button_pressed:  # Scroll wheel up for additional action (e.g., move up), and check if scroll button is not pressed already
        gamepad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NORTH)  # Emulate pressing up on directional pad
        gamepad.update()
        scroll_button_pressed = True  # Set scroll button state to pressed

def release_mouse_button(event=None):
    global scroll_button_pressed
    
    if event is None:
        return
    
    if event.num == 1:  # Left mouse button released
        gamepad.left_trigger_float(value_float=0.0)  # Release L2 button (left trigger)
        gamepad.update()
    elif event.num == 3:  # Right mouse button released
        gamepad.right_trigger_float(value_float=0.0)  # Release R2 button (right trigger)
        gamepad.update()
    elif event.num == 2:  # Scroll wheel button released
        if scroll_button_pressed:
            gamepad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NONE)  # Release directional pad
            gamepad.update()
            scroll_button_pressed = False  # Reset scroll button state

# Function to emulate key press on the keyboard
def emulate_keyboard_press(event):
    if event.char in key_to_button_mapping:
        buttons = key_to_button_mapping[event.char]
        if isinstance(buttons, list):
            for button in buttons:
                gamepad.press_button(button)
        else:
            gamepad.press_button(buttons)
        gamepad.update()
    
# Function to emulate key release on the keyboard
def emulate_keyboard_release(event):
    if event.char in key_to_button_mapping:
        buttons = key_to_button_mapping[event.char]
        if isinstance(buttons, list):
            for button in buttons:
                gamepad.release_button(button)
        else:
            gamepad.release_button(buttons)
        gamepad.update()
    
    # When a key is released, set analog values to 0
    emulate_left_analog_movement(0.0, 0.0)

# Function to emulate keyboard movement for second analog
def emulate_keyboard_movement(event):
    key = event.keysym.lower()
    if key in ["w", "a", "s", "d"]:
        x, y = 0.0, 0.0
        if key == "w":
            y = -1.0
        elif key == "s":
            y = 1.0
        elif key == "a":
            x = -1.0
        elif key == "d":
            x = 1.0
        emulate_left_analog_movement(x, y)
    else:
        # If any other key is pressed, set analog values to 0
        emulate_left_analog_movement(0.0, 0.0)

# Function to emulate movement for second analog
def emulate_left_analog_movement(x, y):
    gamepad.left_joystick_float(x_value_float=x, y_value_float=y)
    gamepad.update()

# Initialize a dictionary to store the mapping of arrow buttons to their corresponding values
arrow_buttons_mapping = {
    "tab": "DS4_BUTTON_DPAD_SOUTH",  # Map the Tab key to the South directional pad button
    "b": "DS4_BUTTON_DPAD_WEST",      # Map the B key to the West directional pad button
    "4": "DS4_BUTTON_DPAD_EAST"       # Map the 4 key to the East directional pad button
}

# Initialize a dictionary to store the states of arrow buttons
arrow_buttons_pressed = {}

# Function to handle key presses on the keyboard
def handle_key_event(event):
    emulate_keyboard_press(event)
    emulate_keyboard_movement(event)
    
    # Check if an arrow button is pressed
    if event.keysym.lower() in arrow_buttons_mapping:
        button = arrow_buttons_mapping[event.keysym.lower()]
        if button not in arrow_buttons_pressed or not arrow_buttons_pressed[button]:
            gamepad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS[button])  # Emulate pressing the arrow button
            gamepad.update()
            arrow_buttons_pressed[button] = True  # Set the state of the button to pressed

# Function to handle key releases on the keyboard
def handle_key_release(event):
    emulate_keyboard_release(event)
    
    # Check if an arrow button is released
    if event.keysym.lower() in arrow_buttons_mapping:
        button = arrow_buttons_mapping[event.keysym.lower()]
        if button in arrow_buttons_pressed and arrow_buttons_pressed[button]:
            gamepad.directional_pad(direction=vg.DS4_DPAD_DIRECTIONS.DS4_BUTTON_DPAD_NONE)  # Emulate releasing the arrow button
            gamepad.update()
            arrow_buttons_pressed[button] = False  # Set the state of the button to released

# Bind keyboard events to corresponding functions
window.bind("<KeyPress>", handle_key_event)
window.bind("<KeyRelease>", handle_key_release)

# Bind mouse button press and release events to corresponding functions
window.bind("<ButtonPress>", emulate_mouse_click)
window.bind("<ButtonRelease>", release_mouse_button)

# Bind mouse and keyboard events to corresponding emulation functions
window.bind("<Button-1>", lambda event: emulate_mouse_click(event))
window.bind("<Motion>", lambda event: mouse_to_joystick(event.x_root, event.y_root))

# Start the Tkinter event loop
window.mainloop()
