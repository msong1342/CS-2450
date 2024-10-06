import customtkinter as ctk
from tkinter import filedialog, messagebox, Menu
import UVSIM as UVSimFile
import json
import colorsys
import re


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UVSim")

        self.uvsim = UVSimFile.UVSim(
            self.read_from_gui,
            self.write_to_accumulator,
            self.set_register_value,
            self.update_gui,
            self.update_memory_display,
            self.update_values_display,
            self.update_console_log
        )

        self.text_box_rotate = 0.25
        self.primary_color = ""
        self.off_color = ""
        self.load_color_scheme()

        self.textbox_color = self.rotate_color(
            self.primary_color, self.text_box_rotate)
        self.hover_color = self.rotate_color(
            self.off_color, rotation_value=0.08)

        self.button_text_color = self.get_text_color(self.off_color)
        self.box_text_color = self.get_text_color(self.textbox_color)

        self.configure(fg_color=self.primary_color)

        self.current_file_path = None

        self.setup_frames()
        self.setup_left_frame()
        self.setup_right_frame()

        self.update_values_display()
        self.create_menu()

    def read_from_gui(self, prompt):  # Requires "{sign}XXXXXX" format
        input_value = ctk.CTkInputDialog(
            text="Enter a 6-digit number (+XXXXXX) or (-XXXXXX)",
            title="Input",
            button_fg_color=self.off_color,
            button_text_color=self.button_text_color,
            button_hover_color=self.hover_color,
            fg_color=self.primary_color,
            entry_fg_color=self.textbox_color,
            entry_text_color=self.box_text_color,
            text_color=self.get_text_color(self.primary_color)
        ).get_input()

        if input_value is None:
            return None
        if len(input_value) == 7 and input_value[1:].isdigit() and (input_value[0] == "-" or input_value[0] == "+"):
            return input_value
        else:
            messagebox.showerror(
                "Invalid Input", "Enter a 6-digit number (+XXXXXX) or (-XXXXXX)"
            )
            return self.read_from_gui(prompt)

    def setup_frames(self):
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.configure(fg_color=self.primary_color)
        self.left_frame.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.configure(fg_color=self.primary_color)
        self.right_frame.grid(row=0, column=1, padx=0, pady=0, sticky='nsew')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

    def setup_left_frame(self):
        # Configure left frame grid
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(1, weight=0)

        # Left frame components
        self.addresses = ctk.CTkTextbox(self.left_frame)
        self.addresses.configure(
            state='normal',
            font=("Verdana", 16),
            fg_color=self.rotate_color(
                self.primary_color, self.text_box_rotate),
            text_color=self.box_text_color
        )
        self.addresses.grid(padx=20, pady=20, row=0, column=0, sticky='nsew')

        self.button_frame = ctk.CTkFrame(self.left_frame)
        self.button_frame.configure(fg_color=self.primary_color)
        self.button_frame.grid(pady=20, padx=20, row=1,
                               column=0, sticky="nsew")

        # Run button
        self.run_button = ctk.CTkButton(
            self.button_frame,
            text='Run',
            command=self.run,
            fg_color=self.off_color,
            text_color=self.button_text_color,
            hover_color=self.hover_color
        )
        self.run_button.pack(side="right", padx=5)

        # Save button
        self.save_button = ctk.CTkButton(
            self.button_frame,
            text='Save',
            command=self.save_file,
            fg_color=self.off_color,
            text_color=self.button_text_color,
            hover_color=self.hover_color
        )
        self.save_button.pack(side="left", padx=5)

        # New Window button
        self.save_as_button = ctk.CTkButton(
            self.button_frame,
            text='New Window',
            command=self.new_window,
            fg_color=self.off_color,
            text_color=self.button_text_color,
            hover_color=self.hover_color
        )
        self.save_as_button.pack(side='left', padx=5)

    def new_window(self):
        app = App()
        app.mainloop()

    def setup_right_frame(self):
        # Right frame grid configuration
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_rowconfigure(2, weight=1)
        self.right_frame.grid_rowconfigure(3, weight=1)

        # Right frame components
        # Console/output box
        self.console = ctk.CTkTextbox(
            self.right_frame,
            height=int(0.7 * self.winfo_height())
        )
        self.console.configure(
            state='disabled',
            font=("Verdana", 12),
            fg_color=self.rotate_color(
                self.primary_color, self.text_box_rotate),
            text_color=self.box_text_color
        )
        self.console.grid(
            padx=20, pady=(20, 0), row=0,
            column=0, columnspan=2, sticky='nsew'
        )

        # options
        self.options_frame = ctk.CTkFrame(
            self.right_frame, width=int(0.8 * self.winfo_width())
        )
        self.options_frame.configure(fg_color=self.primary_color)
        self.options_frame.grid(
            padx=20, pady=20, row=2,
            column=0, columnspan=2, sticky='n'
        )

        # textbox
        self.values_textbox = ctk.CTkTextbox(
            self.options_frame, height=int(0.4 * self.winfo_height())
        )
        self.values_textbox.grid(
            padx=20, pady=20, row=0, column=0, sticky='nsew'
        )
        self.values_textbox.insert('1.0', f'Accumulator: \n')
        self.values_textbox.insert('2.0', f'\nCurrent Register: ')
        self.values_textbox.insert('3.0', f'\nPrinted Number: ')
        self.values_textbox.configure(
            state='disabled',
            font=("Verdana", 12),
            fg_color=self.rotate_color(
                self.primary_color, self.text_box_rotate),
            text_color=self.box_text_color
        )

        self.accumulator_value = 0
        self.register_value = 0
        self.results_value = ""

        # File Input
        self.file_input_button = ctk.CTkButton(
            self.options_frame,
            text='Input file',
            command=self.file_input,
            width=int(0.4 * self.winfo_width()),
            fg_color=self.off_color,
            text_color=self.button_text_color,
            hover_color=self.hover_color
        )
        self.file_input_button.grid(row=0, column=1, padx=5, pady=5)

        # settings button
        self.settings_button = ctk.CTkButton(
            self.right_frame,
            text='Settings',
            command=self.open_settings,
            fg_color=self.off_color,
            text_color=self.button_text_color,
            hover_color=self.hover_color
        )
        self.settings_button.grid(
            row=3, column=0, padx=10, pady=(0, 20), sticky='se')

        # Reset button
        self.reset_button = ctk.CTkButton(
            self.right_frame,
            text='Reset UVSim',
            command=self.reset,
            fg_color=self.off_color,
            text_color=self.button_text_color,
            hover_color=self.hover_color
        )
        self.reset_button.grid(row=3, column=1, padx=20,
                               pady=(0, 20), sticky='se')

    def create_menu(self):
        menu = Menu(self)
        self.config(menu=menu)

        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="Open", command=self.file_input)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)

        menu.add_cascade(label="File", menu=file_menu)

    def run(self):
        # Save edits before running
        self.save_edits()

        # Clear console & values - incase running program after already running a program
        # clear console
        self.console.configure(state='normal')
        self.console.delete('1.0', 'end')
        self.console.configure(state='disabled')
        # reset accumulator and register values
        self.accumulator_value = 0
        self.register_value = 0
        self.results_value = ""

        self.update_values_display()
        self.uvsim.run()
        self.update_console_log()

    # Save edits method
    def save_edits(self):
        content = self.addresses.get('1.0', 'end-1c').splitlines()

        self.uvsim.instructions.clear()
        for i in range(250):
            key = f"{i:03}"
            self.uvsim.registers[key] = 0

        for i, line in enumerate(content):
            line = line.strip()
            if i < 250 and len(line) == 7 and line[1:].isdigit() and (line[0] == "-" or line[0] == "+"):
                self.uvsim.registers[f"{i:03}"] = int(line)
                self.uvsim.instructions.append(line)
            else:
                self.uvsim.instructions.append("+000000")

        self.uvsim.update_memory_display_func()

    # File Input
    def file_input(self):
        file_path = filedialog.askopenfilename()

        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()

            self.addresses.configure(
                state='normal',
                fg_color=self.rotate_color(self.primary_color, 0.25)
            )
            self.addresses.delete('1.0', 'end')
            self.addresses.insert('1.0', content)
            self.addresses.configure(state='normal')

            self.current_file_path = file_path
            self.uvsim.load_file(file_path)
            self.update_console_log()

    def save_file(self):
        content = self.addresses.get('1.0', 'end-1c')

        if len(content.splitlines()) > 250:
            messagebox.showerror(
                "Error", "File exceeds the maximum data size (250 entries)."
                "Error", "File exceeds the maximum data size (250 entries)."
            )
            return

        if self.current_file_path:
            with open(self.current_file_path, 'w') as file:
                file.write(content)
            messagebox.showinfo("Success", "File saved successfully.")
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text files", "*.txt")]
        )

        if file_path:
            content = self.addresses.get('1.0', 'end-1c')

            if len(content.splitlines()) > 250:
                messagebox.showerror(
                    "Error", "File exceeds the maximum data size (250 entries)."
                    "Error", "File exceeds the maximum data size (250 entries)."
                )
                return

            with open(file_path, 'w') as file:
                file.write(content)
            self.current_file_path = file_path
            messagebox.showinfo("Success", "File saved successfully.")

    def reset(self):
        self.uvsim.reset()

        # clear console
        self.console.configure(state='normal')
        self.console.delete('1.0', 'end')
        self.console.configure(state='disabled')

        # reset accumulator and register values
        self.accumulator_value = 0
        self.register_value = 0
        self.results_value = ""

        self.uvsim.reset()

        # reset textboxes and other widgets
        self.addresses.configure(state='normal')
        self.addresses.delete('1.0', 'end')
        self.addresses.configure(state='normal')

        self.values_textbox.configure(state='normal')
        self.values_textbox.delete('1.0', 'end')
        self.values_textbox.insert('1.0', f'Accumulator: \n')
        self.values_textbox.insert('2.0', f'Current Register: ')
        self.values_textbox.configure(state='disabled')

        self.update_values_display()

    def rotate_color(self, color, rotation_value):
        # hex to rgb
        rgb_colors = tuple(
            int(color[i:i+2], 16) for i in (1, 3, 5)
        )

        # rgb to hls -> (hue, lightness, saturation)
        hls_colors = colorsys.rgb_to_hls(*[j/255 for j in rgb_colors])

        if hls_colors[1] < 0.5:  # decimal lightness percentage
            new_lightness = hls_colors[1] + rotation_value
        else:
            new_lightness = hls_colors[1] - rotation_value

        # altered hls to rgb
        new_rgb = colorsys.hls_to_rgb(
            hls_colors[0], new_lightness, hls_colors[2]
        )

        new_rgb = [(int(k*255)) for k in new_rgb]
        r, g, b = new_rgb

        # rgb to hex
        return f"#{r:02x}{g:02x}{b:02x}"

    def get_text_color(self, color):
        # hex to rgb
        rgb_colors = tuple(
            int(color[i:i+2], 16) for i in (1, 3, 5)
        )

        # rgb to hls -> (hue, lightness, saturation)
        hls_colors = colorsys.rgb_to_hls(*[j/255 for j in rgb_colors])
        if hls_colors[1] < 0.5:  # decimal lightness percentage
            return "#FFFFFF"
        return "#000000"

    def open_settings(self):
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("300x400")
        settings_window.configure(fg_color=self.primary_color)

        def save_colors():
            primary_color = color_chooser_primary.get()
            if not valid_hex(primary_color):
                primary_color = "#4C721D"

            off_color = color_chooser_off.get()
            if not valid_hex(off_color):
                off_color = '#FFFFFF'

            with open('color_scheme.json', 'w') as file:
                json.dump(
                    {
                        'primary_color': primary_color,
                        'off_color': off_color,
                    },
                    file
                )

            settings_window.destroy()
            self.load_color_scheme()
            self.update_color_scheme()

        def reset_colors():
            with open('color_scheme.json', 'w') as file:
                json.dump(
                    {
                        'primary_color': "#4C721D",
                        'off_color': "#FFFFFF",
                    }, file
                )

            settings_window.destroy()
            self.load_color_scheme()
            self.update_color_scheme()

        def valid_hex(code):
            hex_pattern = r"^#[A-Fa-f0-9]{6}$|^#[A-Fa-f0-9]{3}$"
            if re.match(hex_pattern, code):
                return True
            return False

        ctk.CTkLabel(
            settings_window,
            text="Primary Color:",
            text_color=self.get_text_color(self.primary_color)
        ).pack(pady=5)

        color_chooser_primary = ctk.CTkEntry(settings_window)
        color_chooser_primary.pack(pady=5)
        color_chooser_primary.insert(0, self.primary_color)
        color_chooser_primary.configure(
            fg_color=self.textbox_color,
            text_color=self.box_text_color
        )

        ctk.CTkLabel(
            settings_window,
            text="Off Color:",
            text_color=self.get_text_color(self.primary_color)
        ).pack(pady=5)

        color_chooser_off = ctk.CTkEntry(settings_window)
        color_chooser_off.pack(pady=5)
        color_chooser_off.insert(0, self.off_color)
        color_chooser_off.configure(
            fg_color=self.textbox_color,
            text_color=self.box_text_color
        )

        # Save Colors
        ctk.CTkButton(
            settings_window,
            text="Save",
            command=save_colors,
            fg_color=self.off_color,
            text_color=self.button_text_color,
            hover_color=self.hover_color
        ).pack(pady=(20, 10))

        # Reset Colors
        ctk.CTkButton(
            settings_window,
            text="Reset Colors",
            command=reset_colors,
            fg_color=self.off_color,
            text_color=self.button_text_color,
            hover_color=self.hover_color
        ).pack(pady=(10, 20))

    def load_color_scheme(self):
        try:
            with open('color_scheme.json', 'r') as file:
                colors = json.load(file)

            self.primary_color = colors['primary_color']
            self.off_color = colors['off_color']
            self.hover_color = self.rotate_color(
                self.off_color, rotation_value=0.08)
            self.textbox_color = self.rotate_color(
                self.primary_color, self.text_box_rotate)
            self.button_text_color = self.get_text_color(self.off_color)
            self.box_text_color = self.get_text_color(self.textbox_color)

        except (FileNotFoundError, KeyError):
            self.primary_color = "#4C721D"
            self.off_color = "#FFFFFF"

    def update_color_scheme(self):
        buttons = [self.run_button, self.save_button, self.save_as_button,
                   self.file_input_button, self.settings_button, self.reset_button]
        for button in buttons:
            button.configure(
                fg_color=self.off_color,
                text_color=self.button_text_color,
                hover_color=self.hover_color
            )

        frames = [self.left_frame, self.right_frame,
                  self.button_frame, self.options_frame, self]
        for frame in frames:
            frame.configure(fg_color=self.primary_color)

        textboxes = [self.values_textbox, self.addresses, self.console]
        for box in textboxes:
            box.configure(fg_color=self.rotate_color(
                self.primary_color, self.text_box_rotate), text_color=self.box_text_color)

    def update_values_display(self):
        # Update display with current accumulator and register values
        self.values_textbox.configure(state='normal')
        self.values_textbox.delete('1.0', 'end')
        self.values_textbox.insert(
            '1.0', f'Accumulator: {self.accumulator_value}\n'
        )
        self.values_textbox.insert(
            '2.0', f'Current Register: {self.register_value:06d}\n'
        )
        self.values_textbox.configure(state='disabled')

    def set_accumulator_value(self, value):
        self.accumulator_value = value
        self.update_values_display()

    def set_register_value(self, value):
        self.register_value = value
        self.update_values_display()

    def write_to_accumulator(self, content):
        self.set_accumulator_value(content)
        self.results_value = content
        self.update_values_display()

    def update_gui(self):
        self.write_to_accumulator(self.accumulator_value)
        self.set_register_value(self.register_value)

    def update_console_log(self):
        log = self.uvsim.get_log()

        self.console.configure(state='normal')
        self.console.delete('1.0', 'end')

        for entry in log:
            self.console.insert('end', f'{entry}\n')

        self.console.configure(state='disabled')

    def update_memory_display(self):
        self.addresses.configure(state='normal')
        self.addresses.delete('1.0', 'end')
        for i in range(250):
            key = f"{i:03}"
            value = self.uvsim.registers[key]
            # Format the value to keep the sign and ensure it is 6 digits
            formatted_value = f"{value:+07d}"
            self.addresses.insert('end', f"{formatted_value}\n")
        self.addresses.configure(state='normal')


if __name__ == '__main__':
    app = App()

    app.mainloop()
