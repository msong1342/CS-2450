# '''
# Software Engineering
# Group I
# UVSIM
# '''

class UVSim:
    def __init__(self, read_func, write_func, update_register_func, update_gui_func, update_memory_display_func, update_console_log, update_values_display) -> None:
        self.read_func = read_func
        self.write_func = write_func
        self.update_register_func = update_register_func
        self.update_gui_func = update_gui_func
        self.update_memory_display_func = update_memory_display_func
        self.update_console_log_func = update_console_log
        self.update_values_display_func = update_values_display
        self.instructions = []
        self.registers = {}
        for i in range(250):
            key = f"{i:03}"
            self.registers[key] = 0
        self.counter = 0
        self.accumulator = 0
        self.log = []

    def run(self):
        self.initialize()
        while self.counter < len(self.instructions):
            prev_counter = self.counter
            self.__execute_instruction()
            if self.counter == prev_counter:  # Only increment if no branch occurred
                self.counter += 1
        self.update_memory_display_func()

    def reset(self):
        self.instructions = []
        for i in range(250):
            key = f"{i:03}"
            self.registers[key] = 0
        self.counter = 0
        self.accumulator = 0
        self.log = []

    def initialize(self):
        self.counter = 0
        self.accumulator = 0
        self.log = []

    def __execute_instruction(self):
        if self.counter >= len(self.instructions):
            return
        instruction = str(self.instructions[self.counter])
        # Instruction = +0XXZZZ - X = command - Z = target
        command = instruction[2:4]
        target = instruction[4:7]
        # Debug print
        print(
            f"Processing command: {self.instructions[self.counter]} | command: {command}, target: {target}")

        match command:
            case '10':  # READ
                value = int(self.read_func(
                    f"Enter value for memory location {target}:"))
                self.registers[target] = value
                self.instructions[int(target)] = value

            case '11':  # WRITE
                value = self.registers[target]
                self.write_func(f"{value:+05d}")
                self.log.append(f"{value:+05d}")

            case '20':  # LOAD
                self.accumulator = self.registers[target]

            case '21':  # STORE
                self.registers[target] = self.accumulator
                self.instructions[int(target)] = self.accumulator

            case '30':  # ADD
                num = int(self.registers[target])
                self.accumulator = (self.accumulator + num) % 1000000
                if self.accumulator > 999999:
                    self.accumulator -= 1000000

            case '31':  # SUBTRACT
                num = int(self.registers[target])
                self.accumulator = (self.accumulator - num) % 1000000
                if self.accumulator < -999999:
                    self.accumulator += 1000000

            case '32':  # DIVIDE
                num = int(self.registers[target])
                self.accumulator //= num

            case '33':  # MULTIPLY
                num = int(self.registers[target])
                self.accumulator = (self.accumulator * num) % 1000000
                if self.accumulator > 999999:
                    self.accumulator -= 1000000

            case '40':  # BRANCH
                self.counter = int(target) - 1

            case '41':  # BRANCHNEG
                if self.accumulator < 0:
                    self.counter = int(target) - 1

            case '42':  # BRANCHZERO
                if self.accumulator == 0:
                    self.counter = int(target) - 1

            case '43':  # HALT
                self.counter = len(self.instructions)

            case '00':  # Empty command - Pass
                pass
            case '0':  # Empty command - Pass
                pass
            case _:
                self.log.append(
                    f"Invalid command: {command} - terminating program")
                self.update_values_display_func()
                raise ValueError('Error: Invalid command: ', command)

        self.update_register_func(self.counter)
        self.write_func(self.accumulator)
        self.update_gui_func()
        self.update_memory_display_func()
        self.update_values_display_func()
        self.update_console_log_func()

    def get_log(self):
        return self.log

    def load_file(self, file_name):
        with open(file_name, 'r', encoding='utf8') as in_file:
            lines = in_file.readlines()
        self.instructions.clear()

        for i, line in enumerate(lines):
            line = line.strip()
            if line:
                sign = ""

                # If sign - set aside sign
                if not line[0].isdigit():
                    sign = line[0]
                    line = line[1:]

                # if line = 4 - convert to 6 digits
                if len(line) == 4:
                    command = line[0:2]
                    target = line[2:4]

                    # Check if its a command or just value
                    if int(command) in [10, 11, 20, 21, 30, 31, 32, 33, 40, 41, 42, 43]:
                        # if command then convert to 0XX0XX format
                        line = str(0) + command + str(0) + target
                    else:
                        # if value then convert to 00XXXX format
                        line = str(0) + str(0) + command + target

                # Add back sign - should now be in this format:
                        # Instruction = +0XXZZZ - X = command - Z = target
                if sign == "-":
                    line = "-" + line
                else:
                    line = "+" + line

                # Store value
                self.instructions.append(line)
                self.registers[f"{i:03}"] = int(line)
            else:
                self.instructions.append("+000000")

        self.update_memory_display_func()
