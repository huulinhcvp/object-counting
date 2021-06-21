import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image
from collections import deque


class Window(ttk.Frame):
    def __init__(self, parent, controller, show_settings):
        super().__init__(parent)

        self["style"] = "Background.TFrame"

        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        
        src_img = controller.src_img
        src_img = ImageTk.PhotoImage(src_img)
        

        settings_button = ttk.Button(
            self,
            text="Settings",
            command=show_settings,
            style="PomodoroButton.TButton",
            cursor="hand2"
        )

        settings_button.grid(row=0, column=1, sticky="E", padx=10, pady=(10, 0))

        btn_img = ttk.Button(self, text ='open image', command=self.open_img)

        btn_img.grid(row=0, column=0, sticky="W", padx=(10, 0), pady=(10, 0))

        timer_frame = ttk.Frame(self, height="100", style="Timer.TFrame")
        timer_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="NSEW")

        self.panel_img = ttk.Label(
            timer_frame,
            image=src_img,
        )
        self.panel_img.image = src_img
        self.panel_img.pack(fill = "both", expand = "yes")
        
        
    def open_img(self):
        src_img = self.controller.open_img()
        
        # PhotoImage class is used to add image to widgets, icons etc
        src_img = ImageTk.PhotoImage(src_img)
        self.panel_img.configure(image=src_img)
        self.panel_img.image = src_img
        
    def update(self):
        src_img = self.controller.src_img
        src_img = ImageTk.PhotoImage(src_img)
        self.panel_img.configure(image=src_img)
        self.panel_img.image = src_img
        