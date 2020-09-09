# 32x8 LED Matrix Controller - Raspberry Pi

Controlling display of MAX7219 32x8 LED Matrix with Raspberry Pi. Included module contains basic functions for message display and animation (including scrolling and real-time-clock)

## Contents
- **`matrix_module.py`:** Matrix class; contains all display and control functions.  
- **`matrix_main.py`:** "Execution File"; imports matrix_module; user should write commands here.
- **`matrix_commented.py`:** Same as matrix_module, but in-depth, line-by-line comments included.  
- **`font.py`:** Hexadecimal definitions (dictionary) for characters. 
    - Key = Character.
    - Value = List of hex strings - each item in list defines a column on the matrix.  
- **`MAX-7219 DataSheet.pdf`:** Data sheet for LED matrix.

## Dependencies
- NumPy - 32x8 ndarray
- RPi.GPIO - Controlling Raspberry Pi
- *NOTE*: Do **NOT** need to enable SPI on RPi

## Usage
### *Pin Setup:*
- VCC - 2, 4
- GND - 6, 9, 14, 20, 25
- DIN - 19 
- CS - 24
- CLK - 23
### *Code:*
- Commands should be written `matrix_main.py` 
- Refer to `matrix_commented.py` or **Docs** section of this file

## Main Functions (`matrix_module.py`)
*\_init\_:* sets up GPIO and creates numpy array which represents LED Matrix
*\_call\_:* splits numpy array into rows of 8 (1 byte) which can be sent to the LED Matrix


## Planned Updates
- Video previews for each display function
- GUI or Application-based control
- More display functions
- Demo program
