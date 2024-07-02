import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as font
from gui.containerframe import ContainerFrame
from gui.fileframes import FileFrame, ScaleFrame
from gui.helperframes import MainHelpFrame
from core.fileinteraction import FileValidation
import pandas as pd


class MainFrame(ContainerFrame):
    """
    MainFrame is a central component of a GUI application designed to manage user interactions and interface layout.

    This class initializes and organizes the main graphical components such as buttons, labels, and frames. It handles user profiles, allowing for creation if none exist, and supports switching between different application modes like 'analyse' or 'rate'. Additionally, it provides help and guidance to users through a dedicated help frame.

    The MainFrame class serves as the backbone for managing the overall user interface and interaction flow of the application, ensuring a seamless user experience.
    """

    def __init__(self, container):
        """
        Initializes the MainFrame which is a container for various interactive elements and frames.

        This method sets up the main GUI components including buttons, labels, and frames. It configures styles,
        handles the creation of a profile if none exists, and organizes the layout of the main interface.

        Args:
            container (tk.Tk): The main application window which acts as the container for this frame.
        """
        super().__init__(container)
        container.style.configure('MainFrame.TButton', font='Arial 25',
            foreground='black')
        if container.dbinteraction.active_profile == '':
            self.no_profile()
        center_container = ttk.Frame(self, style='Card', padding=(5, 6, 7, 8))
        left_frame = ttk.Frame(center_container)
        vert_separator = ttk.Separator(center_container, orient='vertical')
        right_frame = ttk.Frame(center_container)
        general_info = ttk.Label(center_container, font='Arial 20', text=
            'Importiere einen Datensatz und ...')
        analyse_info = ttk.Label(left_frame, font='Arial 20', text=
            '... führe eine Intra-, bzw. Inter-Rater-Analyse durch:')
        analyse_buton = ttk.Button(left_frame, text='Analysieren', image=
            container.analyse_icon, compound='left', style=
            'MainFrame.TButton', command=lambda : self.start_mode('analyse'))
        rate_info = ttk.Label(right_frame, font='Arial 20', text=
            """... bewerte den Text, um eine
Intra-Rater-Reliability-Untersuchung zu erstellen:"""
            )
        rate_button = ttk.Button(right_frame, text='Bewerten', image=
            container.rate_icon, compound='left', style='MainFrame.TButton',
            command=lambda : self.start_mode('rate'))
        self.menu_bar.grid(row=0, column=0, sticky='nsew')
        center_container.grid(row=1, column=0, sticky='nsew', padx=15, pady=15)
        general_info.grid(row=0, column=0, columnspan=3, pady=10)
        left_frame.grid(row=1, column=0)
        vert_separator.grid(row=1, column=1, sticky='nsew', pady=50)
        right_frame.grid(row=1, column=2)
        analyse_info.pack(pady=(0, 100))
        analyse_buton.pack(pady=(0, 200), ipadx=10, ipady=10)
        rate_info.pack(pady=(0, 100))
        rate_button.pack(pady=(0, 200), ipadx=10, ipady=10)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        center_container.rowconfigure(1, weight=1)
        center_container.columnconfigure(0, weight=1)
        center_container.columnconfigure(2, weight=1)

    def start_mode(self, mode):
        """
        Switches the application mode and updates the interface accordingly.

        This method sets the application mode based on the provided argument and updates the relevant frame to reflect the new mode.

        Parameters:
            mode (str): The mode to switch to. Expected values are "analyse" or "rate".
        """
        self.container.mode = mode
        self.container.frames['ScaleFrame'].update_frame()
        self.container.show_frame('ScaleFrame')

    def no_profile(self):
        """
        Handles the scenario where no user profile is detected by prompting the user to create a new profile.

        This method creates a new top-level window that allows the user to enter a name for a new profile. If the user attempts to create a profile without providing a name, an error message is displayed. If a name is provided, the profile is created in the database, and the window is closed.
        """

        def start_cmd():
            if len(user_input.get()) == 0:
                messagebox.showerror(title='Profil anlegen', message=
                    'Bitte gib einen Namen an, um ein Profil anzulegen.')
            else:
                self.container.dbinteraction.create_profile(user_input.get())
                profile_window.destroy()
        user_input = tk.StringVar(value='')
        profile_window = tk.Toplevel(self.container)
        profile_window.title('Profil erstellen')
        profile_window.geometry('500x250')
        profile_window.resizable(False, False)
        container_frame = ttk.Frame(profile_window)
        welcome_label = ttk.Label(container_frame, text='Willkommen!', font
            ='Arial 18 bold')
        profile_label = ttk.Label(container_frame, text=
            """Es wurde noch kein Profil angelegt.
Wie möchtest du heißen?""",
            font='Arial 16')
        input_container = ttk.Frame(container_frame)
        name_label = ttk.Label(input_container, text='Name:', font=
            'Arial 16', image=self.container.face_icon, compound='left')
        input = ttk.Entry(input_container, textvariable=user_input)
        start_button = ttk.Button(container_frame, text='Starten', command=
            start_cmd)
        container_frame.pack(fill='both', expand=True)
        welcome_label.grid(row=0, column=0, sticky='nsew', padx=15, pady=(
            10, 5))
        profile_label.grid(row=1, column=0, sticky='nsew', padx=15, pady=5)
        input_container.grid(row=2, column=0, sticky='nsew', padx=15, pady=20)
        name_label.pack(side='left', padx=(60, 0))
        input.pack(side='right', padx=(0, 60))
        start_button.grid(row=3, column=0, padx=15, pady=8)
        container_frame.columnconfigure(0, weight=1)

    def help_cmd(self, event=None):
        """
        This method, when called, creates and displays the main help frame for the application.

        :param event: Optional event parameter for handling events, defaults to None.
        """
        MainHelpFrame(self.container)
