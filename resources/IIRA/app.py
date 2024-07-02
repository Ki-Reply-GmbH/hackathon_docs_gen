__author__ = 'Timo Kubera'
__email__ = 'timo.kubera@stud.uni-hannover.de'
import os
import tkinter as tk
from tkinter import ttk
from gui.mainframe import MainFrame
from gui.fileframes import FileFrame, ScaleFrame
from gui.analyseframe import AnalyseFrame, ResultsFrame
from gui.rateframe import RateFrame
from core.fileinteraction import DBInteraction
from PIL import ImageTk
file_path = os.path.dirname(os.path.realpath(__file__))


class App(tk.Tk):
    """
    The `App` class is designed to manage the graphical user interface of the IIRA system, handling the initialization and dynamic management of frames, icons, and the main application window.

    This class provides methods to initialize the application, including setting up the main window, loading necessary icons, and configuring frames for different functionalities within the application. It allows for switching between different frames dynamically, ensuring a smooth user experience.
    """

    def __init__(self):
        """
        Initializes the main application window for the IIRA system.

        This method sets up the main window with a title, geometry, and minimum size. It configures the grid layout, initializes the database interaction, loads icons, and sets the theme for the application. It also initializes all frames used in the application and displays the main frame.
        """
        super().__init__()
        self.load_icons()
        self.filevalidation = None
        self.dbinteraction = DBInteraction(os.path.join(file_path,
            'data/internal_db.csv'))
        self.scale_format = ''
        self.weights = ''
        self.categories = []
        self.rater_ids = []
        self.text = []
        self.formatted_text = []
        self.labels = {}
        self.title('IIRA')
        self.geometry('1500x750')
        self.minsize(1450, 750)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.light_mode = True
        self.mode = None
        self.tk.call('source', os.path.join(file_path,
            'data/themes/forest-light.tcl'))
        self.style = ttk.Style()
        self.style.theme_use('forest-light')
        self.frames = {}
        self.init_frames()
        self.show_frame('MainFrame')

    def show_frame(self, frame_name):
        """
        Raises the specified frame to the top of the stack in the application window.

        Args:
            frame_name (str): The name of the frame to be raised.
        """
        frame = self.frames[frame_name]
        frame.tkraise()

    def load_icons(self):
        """
        Loads and initializes all the icons used in the application from the specified file paths.

        This method sets up various icons for the application interface, including icons for app logo, file selection, home, profile, help, face, rate, analyse, tooltip, save, delete, light mode, dark mode, unchecked, and checked states. These icons are loaded as `ImageTk.PhotoImage` objects and are stored as attributes of the App class.
        """
        self.app_icon = ImageTk.PhotoImage(file=os.path.join(file_path,
            'data/icons/intrarater_512px.png'))
        self.file_select_icon = ImageTk.PhotoImage(file=os.path.join(
            file_path, 'data/icons/file_select.png'))
        self.home_icon = ImageTk.PhotoImage(file=os.path.join(file_path,
            'data/icons/home_32px.png'))
        self.profile_icon = ImageTk.PhotoImage(file=os.path.join(file_path,
            'data/icons/profile_32px.png'))
        self.help_icon = ImageTk.PhotoImage(file=os.path.join(file_path,
            'data/icons/help_32px.png'))
        self.face_icon = ImageTk.PhotoImage(file=os.path.join(file_path,
            'data/icons/face_32px.png'))
        self.rate_icon = ImageTk.PhotoImage(file=os.path.join(file_path,
            'data/icons/rate.png'))
        self.analyse_icon = ImageTk.PhotoImage(file=os.path.join(file_path,
            'data/icons/analyse.png'))
        self.tooltip_icon = ImageTk.PhotoImage(file=os.path.join(file_path,
            'data/icons/tooltip-16px.png'))
        self.save_icon = ImageTk.PhotoImage(file=os.path.join(file_path,
            'data/icons/save_32px.png'))
        self.delete_icon = ImageTk.PhotoImage(file=os.path.join(file_path,
            'data/icons/delete_32px.png'))
        self.light_icon = ImageTk.PhotoImage(file=os.path.join(file_path,
            'data/icons/light_mode_32px.png'))
        self.dark_icon = ImageTk.PhotoImage(file=os.path.join(file_path,
            'data/icons/dark_mode.png'))
        self.unchecked_icon = ImageTk.PhotoImage(file=os.path.join(
            file_path, 'data/themes/forest-light/check-unsel-accent.png'))
        self.checked_icon = ImageTk.PhotoImage(file=os.path.join(file_path,
            'data/themes/forest-light/check-accent.png'))

    def init_root_frame(self, frame):
        """
        Initializes and positions the root frame within the main application window.

        This method sets the provided frame to occupy the entire grid cell at the top-left
        corner of the application window, stretching it to fill the entire space available.

        Args:
            frame (tk.Frame): The frame to be initialized and positioned.
        """
        frame.grid(row=0, column=0, sticky='nsew')

    def init_frames(self):
        """
        Initializes and configures the main frames of the application.

        This method sets up the main frames used in the application by first clearing any existing widgets in each frame and then creating and configuring new instances of each frame type. It ensures that each frame is properly grid positioned and stored in the application's frame dictionary for easy access and management.
        """
        for frame in self.frames:
            for widget in self.frames[frame].winfo_children():
                widget.destroy()
        main_frame = MainFrame(self)
        self.init_root_frame(main_frame)
        self.frames['MainFrame'] = main_frame
        scale_frame = ScaleFrame(self)
        self.init_root_frame(scale_frame)
        self.frames['ScaleFrame'] = scale_frame
        file_frame = FileFrame(self)
        self.init_root_frame(file_frame)
        self.frames['FileFrame'] = file_frame
        rate_frame = RateFrame(self)
        self.init_root_frame(rate_frame)
        self.frames['RateFrame'] = rate_frame
        restults_frame = ResultsFrame(self)
        self.init_root_frame(restults_frame)
        self.frames['ResultsFrame'] = restults_frame
        analyse_frame = AnalyseFrame(self)
        self.init_root_frame(analyse_frame)
        self.frames['AnalyseFrame'] = analyse_frame


if __name__ == '__main__':
    app = App()
    app.mainloop()
