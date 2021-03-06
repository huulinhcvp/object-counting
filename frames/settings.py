import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from counter import CounterGrainsOfRice
from processing import ImageProcessing
import cv2 as cv
import numpy as np

OUTPUT_PATH = "resources/out.jpg"


class Settings(ttk.Frame):
    
    def __init__(self, parent, controller, show_timer):
        super().__init__(parent)

        self["style"] = "Background.TFrame"
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.settings_container = ttk.Frame(
            self,
            padding="30 15 30 15",
            style="Background.TFrame"
        )

        self.settings_container.grid(row=0, column=0, sticky="EW", padx=10, pady=10)

        self.settings_container.columnconfigure(0, weight=1)
        self.settings_container.rowconfigure(1, weight=1)

        pomodoro_label = ttk.Label(
            self.settings_container,
            text="Image Processing Method: ",
            style="LightText.TLabel",
            font=("Helvetica",12)
        )
        
        pomodoro_label.grid(column=0, row=0, sticky="W")
        
        self.image_processing_method_name = tk.StringVar()
        
        processing_method = ttk.Combobox(
            self.settings_container,
            justify="center",
            textvariable=self.image_processing_method_name,
            font=("Helvetica",12)
        )
                              
        processing_method["values"] = ("periodic_denoise", "normal_denoise", "black_white_process", "real_world_object_counting")
        processing_method["state"] = "readonly"  # "normal is the counterpart"

        processing_method.grid(column=1, row=0, sticky="EW")
        processing_method.focus()
        
        submit_btn = ttk.Button(
            self.settings_container,
            text="Submit",
            command=self.handler_submit,
            cursor="hand2"
        )
        
        submit_btn.grid(column=0, row=1, sticky="W")
        
        self.res_str = tk.StringVar(value="")
        
        for child in self.settings_container.winfo_children():
            child.grid_configure(padx=10, pady=10)
            
        self.res_label = ttk.Label(
            self.settings_container,
            textvariable=self.res_str,
            style="LightText.TLabel",
            font=("Helvetica",12)
        )
        
        button_container = ttk.Frame(self, style="Background.TFrame")
        button_container.grid(sticky="EW", padx=10)
        button_container.columnconfigure(0, weight=1)

        timer_button = ttk.Button(
            button_container,
            text="??? Back",
            command=show_timer,
            style="PomodoroButton.TButton",
            cursor="hand2"  # hand1 in some systems
        )

        timer_button.grid(column=0, row=0, sticky="EW", padx=2)

    
    def handler_submit(self):
        
        """
            IMAGE PROCESSING
        """
        
        kernel = self.controller.kernel
        np_img = np.array(self.controller.src_img) # load input images
        
        # convert image from BGR to GRAYSCALE image
        np_img = cv.cvtColor(np_img, cv.COLOR_RGB2BGR)
        
        # image processing
        process = ImageProcessing(kernel, np_img)
        
        
        try:
            if (self.image_processing_method_name.get() == 'real_world_object_counting'):
                output_img, num_of_objects = process.real_world_object_counting()
            elif (self.image_processing_method_name.get() == 'periodic_denoise'):
                output_img, num_of_objects = process.periodic_denoise()
            elif (self.image_processing_method_name.get() == 'normal_denoise'):
                output_img, num_of_objects = process.normal_denoise()
            else:
                output_img, num_of_objects = process.black_white_process()
        except:
            pass
        
        cv.imwrite(OUTPUT_PATH, output_img)
        
        ## show result - number of contours in image
        self.res_str.set(f'Result:  {num_of_objects}')
        
        self.res_label.grid(column=0, row=2, sticky="W")
        self.res_label.grid_configure(padx=10, pady=10)
        
        self.controller.src_img = Image.open(OUTPUT_PATH)

        
    def update(self):
        print('This is a placeholder!!!')
