# Sony PS4 Dualshock Emulator

This Python program emulates the functionality of a Sony PS4 Dualshock controller using a computer mouse and keyboard. It allows users to control games or applications that support gamepad input by translating mouse movements, keyboard presses, and mouse clicks into corresponding gamepad inputs.

## Features:

- **Mouse Emulation**: The program translates mouse movements into joystick movements, allowing users to control the right analog stick of the virtual gamepad.
- **Keyboard Emulation**: Keyboard keys are mapped to various buttons on the virtual gamepad, providing control over different functions.
- **Mouse Button Emulation**: Mouse clicks are translated into button presses on the virtual gamepad, enabling actions like aiming and shooting in games.
- **Directional Pad Emulation**: Certain keyboard keys are mapped to directional pad buttons, allowing navigation and menu selection.
- **Customizable Sensitivity**: Users can adjust the sensitivity of mouse movements and keyboard inputs to suit their preferences.

## Controls Mapping:

- **Mouse Movements**: Control the right analog stick.
- **Left Mouse Button**: Aim (emulates left trigger button).
- **Right Mouse Button**: Shoot (emulates right trigger button).
- **Scroll Wheel Up**: Move up (emulates up arrow button).
- **Tab**: Move down (emulates down arrow button).
- **B**: Move left (emulates left arrow button).
- **4**: Move right (emulates right arrow button).
- **Q**: Left shoulder button.
- **E**: Right shoulder button.
- **X**: Combo of left and right shoulder buttons.
- **F**: Square button.
- **R**: Square button.
- **Spacebar**: Cross button.
- **1, 2, 3, G**: Triangle button.
- **C**: Circle button.
- **V**: Right thumbstick button.

## Dependencies:

- **Python 3**: The program requires Python 3 to run.
- **vgamepad**: Python library for creating virtual gamepads.
- **tkinter**: Python library for creating GUI applications.

## Setup:

1. Install Python 3 on your system.
2. Install the required dependencies using `pip install vgamepad`.
3. Run the Python script.

## Usage:

1. Launch the program.
2. Use the mouse to control the right analog stick.
3. Use keyboard keys to trigger button presses.
4. Left-click to aim, right-click to shoot.
5. Scroll up for additional actions, such as moving up.
6. Use other mapped keys for various functions.

## Notes:

- This is a basic implementation and not yet finalized. Further improvements and features can be added for enhanced functionality.
- Ensure that the program window has focus while using keyboard and mouse inputs for emulation.
- Adjust sensitivity settings in the script according to your preferences.
- The program is designed for Windows but may work on other platforms with appropriate adjustments.