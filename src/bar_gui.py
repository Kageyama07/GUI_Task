import tkinter as tk
from tkinter import font
import yaml
import os


class BarGUI(tk.Tk):
    def __init__(self, config):
        """
        Initialize the BarGUI application with the given configuration.

        Parameters:
            config (dict): Configuration parameters loaded from the config.yaml file.
        """
        super().__init__()
        self.title("Bar Length Controller")
        self.configure(bg=config['colors']['background'])

        # Load configuration parameters
        self.slider_min = config['slider']['min']
        self.slider_max = config['slider']['max']
        self.yaxis_min = config['yaxis']['min']
        self.yaxis_max = config['yaxis']['max']
        self.checkbox_internal_values = config['checkbox_values']
        self.font_family = config['font']['family']
        self.title_font_size = config['font']['title_size']
        self.label_font_size = config['font']['label_size']
        self.colors = config['colors']
        self.layout = config['layout']

        # Initialize variables
        self.slider_value = tk.IntVar(value=self.slider_min)
        self.checkbox_values = [tk.IntVar(value=0) for _ in range(len(self.checkbox_internal_values))]

        # Set custom fonts
        self.title_font = font.Font(family=self.font_family, size=self.title_font_size, weight="bold")
        self.label_font = font.Font(family=self.font_family, size=self.label_font_size)

        # Create the left side frame containing slider and checkboxes
        left_frame = tk.Frame(self, bg=self.colors['background'])
        left_frame.pack(side=tk.LEFT, padx=self.layout['padding'], pady=self.layout['padding'], fill=tk.Y)

        # Center frame inside the left frame for vertical centering of content
        center_frame = tk.Frame(left_frame, bg=self.colors['background'])
        center_frame.pack(expand=True)

        # Control frame for grouping slider and checkboxes
        control_frame = tk.Frame(
            center_frame,
            bg=self.colors['frame_background'],
            bd=2,
            relief=tk.RIDGE,
            padx=self.layout['frame_padding'],
            pady=self.layout['frame_padding']
        )
        control_frame.pack(pady=self.layout['frame_padding'])

        # Slider label
        slider_label = tk.Label(
            control_frame,
            text="Slider",
            font=self.title_font,
            bg=self.colors['frame_background'],
            fg=self.colors['text']
        )
        slider_label.grid(row=0, column=0, pady=self.layout['frame_padding'], padx=self.layout['frame_padding'])

        # Slider widget
        self.slider = tk.Scale(
            control_frame,
            from_=self.slider_max,
            to=self.slider_min,
            orient=tk.VERTICAL,
            variable=self.slider_value,
            command=self.update_bars,
            length=self.layout['slider_length'],
            sliderlength=self.layout['slider_sliderlength'],
            width=self.layout['slider_width'],
            bg=self.colors['slider_background'],
            highlightbackground=self.colors['frame_background'],
            troughcolor=self.colors['trough'],
            fg=self.colors['text']
        )
        self.slider.grid(row=1, column=0, rowspan=12, padx=self.layout['frame_padding'])

        # Checkboxes label
        checkboxes_label = tk.Label(
            control_frame,
            text="Checkboxes",
            font=self.title_font,
            bg=self.colors['frame_background'],
            fg=self.colors['text']
        )
        checkboxes_label.grid(row=0, column=1, pady=self.layout['frame_padding'], padx=self.layout['frame_padding'])

        # Checkboxes
        self.checkboxes = []
        for i in range(len(self.checkbox_internal_values)):
            cb = tk.Checkbutton(
                control_frame,
                text=f"Checkbox {i + 1}",
                variable=self.checkbox_values[i],
                command=self.update_bars,
                font=self.label_font,
                bg=self.colors['frame_background'],
                fg=self.colors['text'],
                selectcolor=self.colors['select']
            )
            cb.grid(row=i + 1, column=1, sticky=tk.W, pady=2, padx=self.layout['frame_padding'])
            self.checkboxes.append(cb)

        # Create the right side frame containing the bars
        right_frame = tk.Frame(self, bg=self.colors['background'])
        right_frame.pack(side=tk.RIGHT, padx=self.layout['padding'], pady=self.layout['padding'], fill=tk.BOTH,
                         expand=True)

        # Canvas for drawing bars
        self.canvas = tk.Canvas(right_frame, bg=self.colors['frame_background'], bd=2, relief=tk.RIDGE)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create left and right bars with initial positions
        self.left_bar = self.canvas.create_rectangle(0, 0, 0, 0, fill=self.colors['bar_left'],
                                                     outline=self.colors['bar_left'])
        self.left_bar_label = self.canvas.create_text(0, 0, text="", fill="white", font=self.label_font)

        self.right_bar = self.canvas.create_rectangle(0, 0, 0, 0, fill=self.colors['bar_right'],
                                                      outline=self.colors['bar_right'])
        self.right_bar_label = self.canvas.create_text(0, 0, text="", fill="white", font=self.label_font)

        # Bind resize event to handle window resizing
        self.bind("<Configure>", self.on_resize)

        # Initial update of bars
        self.update_bars()

    def on_resize(self, event):
        """
        Handle window resize events to adjust the layout and font sizes dynamically.
        """
        # Adjust font size based on window height
        new_size = max(self.label_font_size, int(self.winfo_height() / 50))
        self.title_font.configure(size=new_size)
        self.label_font.configure(size=new_size)
        self.update_bars()

    def update_bars(self, event=None):
        """
        Update the heights and positions of the bars based on the slider value and checkbox selections.
        """
        slider_value = self.slider_value.get()
        checkbox_sum = sum(
            val.get() * internal_val for val, internal_val in zip(self.checkbox_values, self.checkbox_internal_values))

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Calculate maximum bar height, reserving space for labels and padding
        max_bar_height = canvas_height - self.layout['bar_padding']

        # Calculate heights of left and right bars
        left_bar_height = (slider_value - self.yaxis_min) / (self.yaxis_max - self.yaxis_min) * max_bar_height
        right_bar_height = (checkbox_sum - self.yaxis_min) / (self.yaxis_max - self.yaxis_min) * max_bar_height

        # Update left bar position and size
        self.canvas.coords(
            self.left_bar,
            canvas_width // 4 - self.layout['bar_width'] // 2,
            canvas_height - self.layout['bar_padding'] - left_bar_height,
            canvas_width // 4 + self.layout['bar_width'] // 2,
            canvas_height - self.layout['bar_padding']
        )
        self.canvas.coords(self.left_bar_label, canvas_width // 4, canvas_height - self.layout['bar_padding'] // 2)
        self.canvas.itemconfig(self.left_bar_label, text=str(slider_value))

        # Update right bar position and size
        self.canvas.coords(
            self.right_bar,
            3 * canvas_width // 4 - self.layout['bar_width'] // 2,
            canvas_height - self.layout['bar_padding'] - right_bar_height,
            3 * canvas_width // 4 + self.layout['bar_width'] // 2,
            canvas_height - self.layout['bar_padding']
        )
        self.canvas.coords(self.right_bar_label, 3 * canvas_width // 4, canvas_height - self.layout['bar_padding'] // 2)
        self.canvas.itemconfig(self.right_bar_label, text=str(checkbox_sum))


if __name__ == "__main__":
    # Load configuration from config.yaml file
    config_path = os.path.join(os.path.dirname(__file__), '..', 'lib', 'config.yaml')
    with open(config_path, 'r') as stream:
        config = yaml.safe_load(stream)

    # Create and run the BarGUI application
    app = BarGUI(config)
    app.mainloop()
