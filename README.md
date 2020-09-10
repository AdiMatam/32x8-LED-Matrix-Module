# 32x8 LED Matrix Controller - Raspberry Pi

Controlling display of MAX7219 32x8 LED Matrix with Raspberry Pi. Included module contains basic functions for message display and animation (including scrolling and real-time-clock)

## Dependencies
- NumPy - 32x8 ndarray
- RPi.GPIO - Controlling Raspberry Pi
- *NOTE*: Do **NOT** need to enable SPI on RPi

## Contents
- **`matrix_module.py`:** Matrix class; contains all display and control functions.  
- **`matrix_main.py`:** "Execution File"; imports matrix_module; user should write commands here.  
- **`font.py`:** Hexadecimal definitions (dictionary) for characters. 
    - Key = Character.
    - Value = List of hex strings - each item in list defines a column on the matrix.  
- **`MAX-7219 DataSheet.pdf`:** Data sheet for LED matrix.

## Usage
### *Pin Setup:*
- VCC - 2, 4
- GND - 6, 9, 14, 20, 25
- DIN - 19 
- CS - 24
- CLK - 23
### *Code:*
- Commands should be written `matrix_main.py` 
- Refer to **Docs** sections of this file. 
    - In `matrix_module.py`, all functions before "### STATIC ###" annotation can be used.

## Docs and Main Functions (`matrix_module.py`)
`__init__:` sets up GPIO and creates numpy array which represents LED Matrix
`__call__:` splits numpy array into 4 sub-arrays and then into rows of 8 (1 byte) which can be sent to the LED Matrix  

`power_down()`: shuts down the display

`set_col(col, value)`: lights-up one column  
- col -> 0 to 31
- value -> which LEDs in the column should be lit up (integer, hex value, binary value are all acceptable)  

`set_char(loc, char)`: displays one character
- loc -> start column
- char -> "A-z0-9" and some symbols

`static (message)`: shows 'still' message
- message -> string

`scrolled (message, delay)`: scrolls message from right to left
- message -> string
- delay -> refresh rate (shorter delay ==> faster scroll)

`stacked (message, delay, reverse)`: stacks a message, lighting up one row at a time (Try it out!)
- message -> string
- delay -> refresh rate
- reverse -> stack from bottom or top

`run_rtc()`: displays real-time-clock until KeyboardInterrupt invoked

## Planned Updates
- Video previews for each display function
- GUI or Application-based control
- More display functions
- Line-by-line commented program (showing how it works)
