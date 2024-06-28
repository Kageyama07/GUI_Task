import tkinter as tk
from tkinter import font


class BarGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bar Length Controller")
        self.configure(bg="#f0f0f0")

        # Initialize variables
        self.slider_value = tk.IntVar(value=350)
        self.checkbox_values = [tk.IntVar(value=0) for _ in range(12)]
        self.checkbox_internal_values = [50, 40, 30, 20, 10, 60, 70, 80, 90, 100, 110, 120]  # Example values

        # Custom fonts
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=12)

        # Create the left side with slider and checkboxes
        left_frame = tk.Frame(self, bg="#f0f0f0")
        left_frame.pack(side=tk.LEFT, padx=20, pady=20)

        # Slider
        slider_label = tk.Label(left_frame, text="Slider", font=self.title_font, bg="#f0f0f0")
        slider_label.grid(row=0, column=0, pady=10)

        self.slider = tk.Scale(left_frame, from_=750, to=350, orient=tk.VERTICAL,
                               variable=self.slider_value, command=self.update_bars,
                               length=300, sliderlength=30, width=20, bg="#f0f0f0",
                               highlightbackground="#f0f0f0", troughcolor="#d3d3d3")
        self.slider.grid(row=1, column=0, rowspan=12, padx=10)

        # Checkboxes
        checkboxes_label = tk.Label(left_frame, text="Checkboxes", font=self.title_font, bg="#f0f0f0")
        checkboxes_label.grid(row=0, column=1, padx=10, pady=10)

        self.checkboxes = []
        for i in range(12):
            cb = tk.Checkbutton(left_frame, text=f"Checkbox {i + 1}", variable=self.checkbox_values[i],
                                command=self.update_bars, font=self.label_font, bg="#f0f0f0")
            cb.grid(row=i + 1, column=1, sticky=tk.W, pady=2)
            self.checkboxes.append(cb)

        # Create the right side with bars
        right_frame = tk.Frame(self, bg="#f0f0f0")
        right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(right_frame, bg="#ffffff", bd=2, relief=tk.SUNKEN)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.left_bar = self.canvas.create_rectangle(0, 0, 0, 0, fill="#4682B4", outline="")
        self.left_bar_label = self.canvas.create_text(0, 0, text="", fill="black", font=self.label_font)

        self.right_bar = self.canvas.create_rectangle(0, 0, 0, 0, fill="#FF6347", outline="")
        self.right_bar_label = self.canvas.create_text(0, 0, text="", fill="black", font=self.label_font)

        self.bind("<Configure>", self.on_resize)

        self.update_bars()

    def on_resize(self, event):
        self.update_bars()

    def update_bars(self, event=None):
        slider_value = self.slider_value.get()
        checkbox_sum = sum(
            val.get() * internal_val for val, internal_val in zip(self.checkbox_values, self.checkbox_internal_values))

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Calculate bar heights
        left_bar_height = (slider_value - 350) / (750 - 350) * (canvas_height - 30)  # Reserve space for labels
        right_bar_height = checkbox_sum / 750 * (canvas_height - 30)  # Reserve space for labels

        # Update left bar
        self.canvas.coords(self.left_bar, canvas_width // 4 - 25, canvas_height - 30 - left_bar_height,
                           canvas_width // 4 + 25, canvas_height - 30)
        self.canvas.coords(self.left_bar_label, canvas_width // 4, canvas_height - 15)
        self.canvas.itemconfig(self.left_bar_label, text=str(slider_value))

        # Update right bar
        self.canvas.coords(self.right_bar, 3 * canvas_width // 4 - 25, canvas_height - 30 - right_bar_height,
                           3 * canvas_width // 4 + 25, canvas_height - 30)
        self.canvas.coords(self.right_bar_label, 3 * canvas_width // 4, canvas_height - 15)
        self.canvas.itemconfig(self.right_bar_label, text=str(checkbox_sum))


if __name__ == "__main__":
    app = BarGUI()
    app.mainloop()
