#!/usr/bin/python3

# Copyright 2021 Ha Huu Linh, hahuulinh1999@gmail.com

#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tkinter as tk
from tkinter import ttk
from collections import deque
from frames import Window, Settings
from tkinter import filedialog
from PIL import ImageTk, Image
import numpy as np

# all constants in object counting app
COLOUR_PRIMARY = "#2e3f4f"
COLOUR_SECONDARY = "#293846"
COLOUR_LIGHT_BACKGROUND = "#fff"
COLOUR_LIGHT_TEXT = "#eee"
COLOUR_DARK_TEXT = "#8095a8"

DEFAULT_PATH = 'resources/default.jpg'


class ObjectCounting(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        # define style for my app
        style = ttk.Style()
        
        # define theme for app
        style.theme_use("default")

        # customize my own frame
        style.configure("Timer.TFrame", background=COLOUR_LIGHT_BACKGROUND)
        style.configure("Background.TFrame", background=COLOUR_PRIMARY)
        style.configure(
            "TimerText.TLabel",
            background=COLOUR_LIGHT_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font="Courier 38"
        )

        style.configure(
            "LightText.TLabel",
            background=COLOUR_PRIMARY,
            foreground=COLOUR_LIGHT_TEXT,
        )

        style.configure(
            "PomodoroButton.TButton",
            background=COLOUR_SECONDARY,
            foreground=COLOUR_LIGHT_TEXT,
        )

        style.map(
            "PomodoroButton.TButton",
            background=[("active", COLOUR_PRIMARY), ("disabled", COLOUR_LIGHT_TEXT)]
        )
        
        
        # Main app window is a tk widget, so background is set directly
        self["background"] = COLOUR_PRIMARY

        # main app setting
        self.title("Object Counting")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.src_img = Image.open(DEFAULT_PATH) # variables for tracking image label
        self.kernel = np.ones((5,5),np.uint8) # kernel for morphological operators

        container = ttk.Frame(self)
        container.grid()
        container.columnconfigure(0, weight=1)

        self.frames = {}

        settings_frame = Settings(container, self, lambda: self.show_frame(Window))
        window_frame = Window(container, self, lambda: self.show_frame(Settings))
        settings_frame.grid(row=0, column=0, sticky="NESW")
        window_frame.grid(row=0, column=0, sticky="NESW")

        self.frames[Settings] = settings_frame
        self.frames[Window] = window_frame
        
        self.show_frame(Window)
        
        button_container = ttk.Frame(self, style="Background.TFrame")
        button_container.grid(row=1, column=0, columnspan=2, sticky="EW")
        button_container.columnconfigure(0, weight=1)

        self.stop_button = ttk.Button(
            button_container,
            text="Quit",
            command=self.destroy,
            cursor="hand2"
        )

        self.stop_button.grid(row=0, column=0, sticky="EW", padx=5)


    def show_frame(self, container):
        """
            show image frame || settings frame,
            update image frame after processing
        """
        frame = self.frames[container]
        frame.update()
        frame.tkraise()
        

    def open_img(self):
        """
            open image file from file system
        """
        try:
            filename = filedialog.askopenfilename(filetypes=[("Image File",'.jpg .png')])
            self.src_img = Image.open(filename)
            return self.src_img
        except AttributeError:
            print("Please choose one image for processing!!!")
            self.reset_img()
            return self.src_img

    
    def reset_img(self):
        """
            default image
        """
        self.src_img = Image.open(DEFAULT_PATH)


app = ObjectCounting()
app.mainloop()
