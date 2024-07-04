import tkinter as tk
from tkinter import ttk, messagebox
import shutil
import os
from gui.helperframes import ProfileFrame


class ContainerFrame(ttk.Frame):
    """
    ContainerFrame is a class that provides a structured and interactive user interface frame within a Tkinter application.

    This class is designed to manage and display various interactive elements such as a menu bar, tables, and different frames for home, profile, and help sections. It includes methods to handle mouse events, toggle color modes, and update the frame's content dynamically.

    Attributes:
        container (tk.Tk or tk.Frame): The parent container for this frame.

    Methods:
        __init__(container): Initialize the ContainerFrame with the given parent container.
        init_menu_bar(): Initialize the menu bar with interactive frames and labels for "Home", "Profil", and "Hilfe" sections.
        on_enter(frame, label): Handle the event when the mouse pointer enters a frame, changing its style and label background color.
        on_leave(frame, label): Handle the event when the mouse pointer leaves a frame, resetting its style and label background color.
        toggle_color_mode(): Toggle the application's color mode between light and dark themes.
        create_table(parent, headings, content): Create a table with specified headings and content in the given parent widget.
        profile_cmd(): Open the profile frame when the profile menu item is clicked.
        home_cmd(): Handle the command to navigate to the home screen.
        help_cmd(event=None): Display a help message or perform a help-related action when the help button is clicked.
        update_frame(): Update the frame with specific content or settings, intended to be implemented in subclasses.
    """

    def __init__(self, container):
        """
                ""\"
                Initialize the ContainerFrame.

                Args:
                    container (tk.Tk or tk.Frame): The parent container for this frame.
                ""\"
        """
        super().__init__(container)
        self.container = container
        self.accent_color = '#217346'
        container.style.configure('TopFrame.TFrame', background=self.
            accent_color)
        self.menu_bar = ttk.Frame(self)
        self.init_menu_bar()

    def init_menu_bar(self):
        """
        Initialize the menu bar with various interactive frames and labels.

        This method sets up the menu bar with frames and labels for "Home", "Profil", and "Hilfe" sections.
        It binds mouse events to these elements to handle hover and click actions, and arranges them
        using a grid layout.

        The method also includes separators for better visual organization of the menu bar.
        """
        home_frame = ttk.Frame(self.menu_bar, width=65, height=50)
        home_label = ttk.Label(home_frame, text='Home', image=self.
            container.home_icon, compound='top', font='Arial 12')
        home_frame.bind('<Enter>', lambda x: self.on_enter(home_frame,
            home_label))
        home_frame.bind('<Leave>', lambda x: self.on_leave(home_frame,
            home_label))
        home_label.bind('<Button-1>', lambda x: self.home_cmd())
        home_frame.bind('<Button-1>', lambda x: self.home_cmd())
        profile_frame = ttk.Frame(self.menu_bar, width=65, height=50)
        profile_label = ttk.Label(profile_frame, text='Profil', image=self.
            container.profile_icon, compound='top', font='Arial 12')
        profile_frame.bind('<Enter>', lambda x: self.on_enter(profile_frame,
            profile_label))
        profile_frame.bind('<Leave>', lambda x: self.on_leave(profile_frame,
            profile_label))
        profile_label.bind('<Button-1>', lambda x: self.profile_cmd())
        profile_frame.bind('<Button-1>', lambda x: self.profile_cmd())
        horizon_separator = ttk.Separator(self.menu_bar, orient='horizontal')
        vert_separator = ttk.Separator(self.menu_bar, orient='vertical')
        self.help_frame = ttk.Frame(self.menu_bar, width=65, height=50)
        self.help_label = ttk.Label(self.help_frame, text='Hilfe', image=
            self.container.help_icon, compound='top', font='Arial 12')
        self.help_label.bind('<Enter>', lambda x: self.on_enter(self.
            help_frame, self.help_label))
        self.help_label.bind('<Leave>', lambda x: self.on_leave(self.
            help_frame, self.help_label))
        self.help_frame.bind('<Button-1>', self.help_cmd)
        self.help_label.bind('<Button-1>', self.help_cmd)
        home_frame.grid(row=0, column=0, sticky='nsew')
        profile_frame.grid(row=0, column=1, sticky='nsew')
        self.help_frame.grid(row=0, column=3, sticky='nsew')
        horizon_separator.grid(row=1, column=0, columnspan=4, sticky='nsew')
        vert_separator.grid(row=0, column=4, sticky='nsew')
        home_label.place(relx=0.5, rely=0.5, anchor='center')
        profile_label.place(relx=0.5, rely=0.5, anchor='center')
        self.help_label.place(relx=0.5, rely=0.5, anchor='center')

    def on_enter(self, frame, label):
        """
        Handle the event when the mouse pointer enters a frame.

        Args:
            frame (ttk.Frame): The frame that the mouse pointer has entered.
            label (ttk.Label): The label associated with the frame.

        This method changes the style of the frame and the background color of the label to indicate that the mouse pointer is over the frame.
        """
        if frame is not None:
            frame.configure(style='TopFrame.TFrame')
        label['background'] = self.accent_color

    def on_leave(self, frame, label):
        """
        Handle the event when the mouse pointer leaves a frame.

        This method is triggered when the mouse pointer leaves a specified frame. It resets the frame's style and the label's background color to their default values.

        Args:
            frame (ttk.Frame): The frame from which the mouse pointer has left.
            label (ttk.Label): The label associated with the frame.
        """
        if frame is not None:
            frame.configure(style='TFrame')
        label['background'] = ttk.Style().lookup('TFrame', 'background')

    def toggle_color_mode(self):
        """
        Toggle the color mode of the application between light and dark themes.

        This method switches the application's theme based on the current mode. If the 
        application is in light mode, it changes to dark mode and vice versa.

        Attributes:
            None

        Returns:
            None
        """
        if self.container.light_mode:
            self.container.light_mode = False
            self.container.style.theme_use('forest-dark')
        else:
            self.container.light_mode = True
            self.container.style.theme_use('forest-light')

    def create_table(self, parent, headings, content):
        """
        ""\"
        Create a table with the specified headings and content in the given parent widget.

        Args:
            parent (tk.Widget): The parent widget where the table will be created.
            headings (list of str): A list of strings representing the column headings.
            content (list of list): A list of lists where each sublist represents a row of content. 
                                    Each element in the sublist can be a string or a Tkinter variable 
                                    (e.g., for a Checkbutton).

        Returns:
            None
        ""\"
        """
        rowspan = max(len(content) + 2, 2)
        columnspan = max(len(headings) * 2, 2)
        index = 0
        for heading in headings:
            heading_lbl = ttk.Label(parent, text=heading, font='Arial 15 bold')
            heading_lbl.grid(row=0, column=index)
            if heading != headings[-1]:
                vert_separator = ttk.Separator(parent, orient='vertical')
                vert_separator.grid(row=0, column=index + 1, rowspan=
                    rowspan, sticky='nsew', padx=5)
            index += 2
        horizon_separator = ttk.Separator(parent, orient='horizontal')
        horizon_separator.grid(row=1, column=0, columnspan=columnspan,
            sticky='nsew', pady=5)
        for i, row in enumerate(content, start=2):
            index = 0
            for cell in row:
                if isinstance(cell, str):
                    cell_lbl = ttk.Label(parent, text=cell, font='Arial 15')
                    cell_lbl.grid(row=i, column=index, pady=5)
                elif isinstance(cell, list):
                    pass
                else:
                    cell_chkbtn = ttk.Checkbutton(parent, variable=cell)
                    cell_chkbtn.grid(row=i, column=index, pady=5)
                index += 2

    def profile_cmd(self):
        """
        Open the profile frame when the profile menu item is clicked.

        This method is triggered when the user clicks on the profile label or frame in the menu bar. It initializes and displays the ProfileFrame.

        Returns:
            None
        """
        ProfileFrame(self.container)

    def home_cmd(self):
        """
        Handle the command to navigate to the home screen.

        This method initializes the frames and displays the main frame of the application.
        """
        self.container.init_frames()
        self.container.show_frame('MainFrame')

    def help_cmd(self, event=None):
        """
        Display a help message or perform a help-related action when the help button is clicked.

        Args:
            event (tkinter.Event, optional): The event that triggered the help command. Defaults to None.

        Raises:
            NotImplementedError: This method is not yet implemented.
        """
        raise NotImplementedError

    def update_frame(self):
        """
        Update the frame with specific content or settings.

        This method is intended to be implemented in subclasses to provide
        custom functionality for updating the frame's content or settings.
        """
        raise NotImplementedError
