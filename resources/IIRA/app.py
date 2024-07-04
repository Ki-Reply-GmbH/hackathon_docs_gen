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
    The App class serves as the main application window for a graphical user interface (GUI) application.

    This class is responsible for initializing the main window, loading necessary resources such as icons, and managing the various frames that make up the application. It provides methods to display different frames, load icons, and configure the layout of the frames within the main window.

    Attributes:
        filevalidation (None): Placeholder for file validation logic.
        dbinteraction (DBInteraction): Handles database interactions with the internal database.
        scale_format (str): Format of the scale (nominal, ordinal, interval, ratio).
        weights (str): Placeholder for weights.
        categories (list): List of categories.
        rater_ids (list): List of rater IDs.
        text (list): List of text entries.
        formatted_text (list): List of formatted text entries.
        labels (dict): Dictionary of labels for each text and rater.
        light_mode (bool): Indicates if the light mode is active.
        mode (None): Placeholder for the current mode.
        frames (dict): Dictionary of frames used in the application.
        style (ttk.Style): Style object for managing themes.

    Superclass:
        tk.Tk: The App class is derived from the Tk class in the tkinter module, which provides the main window for the application.
    """

    def __init__(self):
        """
        Initializes the App class, setting up the main application window and its components.

        This method performs the following tasks:
        - Calls the parent class (tk.Tk) initializer.
        - Loads application icons.
        - Initializes various attributes related to file validation, database interaction, scale format, weights, categories, rater IDs, text, formatted text, and labels.
        - Sets the window title, size, and minimum size.
        - Configures the main window's row and column weights.
        - Loads the light mode theme and sets it as the current theme.
        - Initializes the frames used in the application and displays the main frame.

        Attributes:
            filevalidation (None): Placeholder for file validation logic.
            dbinteraction (DBInteraction): Handles database interactions with the internal database.
            scale_format (str): Format of the scale (nominal, ordinal, interval, ratio).
            weights (str): Placeholder for weights.
            categories (list): List of categories.
            rater_ids (list): List of rater IDs.
            text (list): List of text entries.
            formatted_text (list): List of formatted text entries.
            labels (dict): Dictionary of labels for each text and rater.
            light_mode (bool): Indicates if the light mode is active.
            mode (None): Placeholder for the current mode.
            frames (dict): Dictionary of frames used in the application.
            style (ttk.Style): Style object for managing themes.
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
        Display the specified frame by bringing it to the front.

        Args:
            frame_name (str): The name of the frame to be displayed.
        """
        frame = self.frames[frame_name]
        frame.tkraise()

    def load_icons(self):
        """
        Loads various icons used in the application from the file system and assigns them to instance variables.
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
        Position the given frame within the root window.

        This method sets the layout configuration for the provided frame by 
        placing it in the root window's grid at row 0 and column 0, and making 
        it expand to fill the available space in all directions.

        Args:
            frame (tk.Frame): The frame to be positioned within the root window.
        """
        frame.grid(row=0, column=0, sticky='nsew')

    def init_frames(self):
        """
        Initialize and configure the main application frames.

        This method sets up the main frames used in the application by creating instances
        of each frame class and adding them to the `frames` dictionary. It also ensures
        that any existing widgets within the frames are destroyed before reinitializing
        the frames.

        The frames initialized include:
        - MainFrame
        - ScaleFrame
        - FileFrame
        - RateFrame
        - ResultsFrame
        - AnalyseFrame
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
