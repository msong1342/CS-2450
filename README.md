# UVSIM - User Guide

## Overview

UVSim is a virtual machine designed for computer science students to learn machine language and computer architecture. It simulates a basic CPU, register, and main memory, and interprets a machine language called BasicML.


## Features

- **CPU and Register**: Includes an accumulator register for calculations.
- **Memory**: Equipped with a 250-word memory.
- **BasicML Instructions**: Supports I/O operations, load/store operations, arithmetic operations, and control operations.
- **GUI**: User-friendly interface for loading, editing, and saving BasicML programs.


## BasicML Vocabulary

- **I/O Operations**:
  - `READ = 10`: Read a word from the keyboard into memory.
  - `WRITE = 11`: Write a word from memory to the screen.

- **Load/Store Operations**:
  - `LOAD = 20`: Load a word from memory into the accumulator.
  - `STORE = 21`: Store a word from the accumulator into memory.

- **Arithmetic Operations**:
  - `ADD = 30`: Add a word from memory to the accumulator.
  - `SUBTRACT = 31`: Subtract a word from memory from the accumulator.
  - `DIVIDE = 32`: Divide the accumulator by a word from memory.
  - `MULTIPLY = 33`: Multiply a word from memory by the accumulator.

- **Control Operations**:
  - `BRANCH = 40`: Branch to a specific memory location.
  - `BRANCHNEG = 41`: Branch to a memory location if the accumulator is negative.
  - `BRANCHZERO = 42`: Branch to a memory location if the accumulator is zero.
  - `HALT = 43`: Stop the program.


## Prerequisites

Ensure you have the following installed:
- Python 3
- `pip install customtkinter`
- `pip install tk`


## Usage Instructions
1. **Clone the Repository**:

   ```sh
   git clone https://github.com/mobj44/CS2450_Group_I
   cd CS2450_Group_I


2. **Run the Simulator**:

   ```sh
   python3 gui.py
   ```


3. **Load a BasicML Program**:

   - Click the 'Input File' button on the bottom right-hand part of the screen for inputting a file.
   - Select the file you want to run through your OS file selector. Any file on your OS is selectable.
   - Once you select a file, the file commands will load up into the left-hand side box.
   - To run the commands, select the 'Run' button located just under the loaded commands box.


3. **Editing the BasicML Program**:

   - The left-hand side box where the file is loaded is editable. You can cut, copy, paste, add, modify, and delete function codes and data values.
   - Ensure the total number of lines does not exceed 250 entries.


4. **Saving the BasicML Program**:
   
   - To save the current file, use the 'Save' Button.


5. **Interacting with the Simulator**:
   
   - The simulation will run until completion of the input file unless input from the user is required.
   - To input a number, a pop-up box named 'Input' will appear asking for a 6-digit value (along with a sign). After typing in your input number, hit the 'OK' button or press enter.
   - The input box does not allow for an empty input, so please enter a valid number.
   - Only input integer values (e.g., 1, 2, 3, 4). The program cannot handle other data types (e.g., 1.33, abcd). Incorrect format input will crash the program, requiring a restart.
   - ***NOTE***: Input box may pop up behind the simulation program window. If you run your program and nothing appears and you know that input is needed please check behind the simulation window to ensure the program is not waiting for input. This happens primarily when multiple inputs are called.
   - If input box will not allow for input after multiple input entries, try clicking on the simulator window and then back to the input box.
   - The simulator will handle input as specified by the user.
   - The simulator will output all output (or WRITE) commands in the top right box. If list of outputted numbers exceeds window size, please scroll down to see full command history list.
   - The simulator will also store 'Accumulator' and 'Current Register' in the lower right hand box.
   -  The program window is resizable, please resize at own interest.


5. **Resetting the Simulator**:

   - To reset the simulator, hit the 'Reset UVSim' located at the bottom right hand side of the window.
   - Hitting this button will close the current simulator window and pop up a new one.
   - Only use this button to completely clean and reset your simulator.
   - If you reset the sim before saving any file then your file will not save.


6. **Saving a file**

   - To edit a file, simply click in the command entries window (left hand side window) and edit directly in the box.
   - To save an edited file, click the 'save' button and the file will save as the original file.


7. **Color Settings**

   - To change the color from the UVU green color, click the 'Settings' button.
   - A pop-up window will appear asking for a hex number for the color of your choice.
   - Please enter only valid hex numbers, visit the following website for examples of valid hex code colors: "https://www.color-hex.com/"
   - Reset to the original UVU colors with the 'Reset Colors' button on the setting window.
   - The program will not allow for incorrect HEX codes.
  
8. **Creating Multiple Open Files**
   - To create a new window to run another file please click the 'New Window' button on the bottom left side of the screen.
   - A new window will automatically pop up and you will be able to run multiple files at once.
   - Open windows will also allow for multiple files to be saved at one time as well.
   - Newly saved files will have to be reopened if they are currently open in another file.
   - Close unwanted windows by simply clicking the 'X' in the top right corner. 


## Contact
For any questions or issues, please contact 
Caleb.zierenberg@gmail.com, morganbjohnston@gmail.com, xjendu12@gmail.com, 10950537@uvu.edu
