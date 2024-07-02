import tkinter as tk
from tkinter import ttk, messagebox
import shutil
import os
from gui.helperframes import ProfileFrame


class ContainerFrame(ttk.Frame):
    """
    A GUI management class designed to operate within a container widget, handling various interactive elements and themes.

    The ContainerFrame class is responsible for initializing and managing a graphical user interface within a specified container. It sets up the frame, configures styles, and initializes a menu bar with interactive elements. The class provides functionality to handle user interactions such as mouse enter and leave events, and commands associated with menu items like 'Home', 'Profile', and 'Help'. Additionally, it supports toggling between light and dark color themes and updating the GUI components dynamically.

    Attributes:
        container (ttk.Widget): The parent widget in which this frame and its components are placed.

    Methods:
        __init__(self, container): Initializes the frame within the given container.
        init_menu_bar(self): Sets up the interactive menu bar.
        on_enter(self, frame, label): Changes styles when the mouse enters a frame or label.
        on_leave(self, frame, label): Restores styles when the mouse leaves a frame or label.
        toggle_color_mode(self): Switches the GUI theme between light and dark modes.
        create_table(self, parent, headings, content): Creates a table with specified headings and content.
        profile_cmd(self): Activates the profile management interface.
        home_cmd(self): Displays the main frame of the application.
        help_cmd(self): Placeholder for help command functionality.
        update_frame(self): Intended to be overridden to update the GUI frame in derived classes.
    """

    def __init__(self, container):
        """
        Initialize the ContainerFrame with a specified container.

        This method sets up the frame within the given container, configures the style, and initializes the menu bar.

        Args:
            container: The parent widget in which this frame will be placed.
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
        Initializes the menu bar for the ContainerFrame by creating and configuring the menu items.

        This method sets up the menu bar with 'Home', 'Profile', and 'Help' sections, each represented by a frame and a label. 
        Each section is interactive, responding to mouse enter and leave events to change styles, and click events to execute specific commands.
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
            ""\"
            Handles the mouse entering an element by changing the frame and label styles.

            This method is triggered when the mouse pointer enters the area of a frame or label.
            It sets the frame's style to a predefined style with an accent color and changes
            the background color of the label to the accent color.

            Parameters:
                frame (ttk.Frame): The frame that the mouse enters.
                label (ttk.Label): The label within the frame whose background color is changed.
            ""\"
        """
        if frame is not None:
            frame.configure(style='TopFrame.TFrame')
        label['background'] = self.accent_color

    def on_leave(self, frame, label):
        """
        Restores the default style and background color of the specified frame and label when the mouse leaves the frame.

        This method is typically bound to the `<Leave>` event of a frame and its associated label. It resets the frame's style to the default 'TFrame' style and sets the label's background color to match the default background color of 'TFrame'.

        Parameters:
            frame (ttk.Frame): The frame that the mouse has left.
            label (ttk.Label): The label within the frame that needs its background color reset.
        """
        if frame is not None:
            frame.configure(style='TFrame')
        label['background'] = ttk.Style().lookup('TFrame', 'background')

    def toggle_color_mode(self):
        """
        Toggles the color mode of the application between light and dark themes.

        This method checks the current state of `container.light_mode`. If it is True, it switches the theme to a dark mode ('forest-dark'). If False, it switches to a light mode ('forest-light'). This change affects the overall appearance of the application's GUI.
        """
        if self.container.light_mode:
            self.container.light_mode = False
            self.container.style.theme_use('forest-dark')
        else:
            self.container.light_mode = True
            self.container.style.theme_use('forest-light')

    def create_table(self, parent, headings, content):
        """
        Creates a table in the specified parent widget using the provided headings and content.

        Args:
            parent (ttk.Widget): The parent widget where the table will be created.
            headings (list): A list of strings representing the column headings.
            content (list of lists): A list where each sublist represents a row of data.

        The table is created with labels for headings and either labels or checkbuttons for each cell,
        depending on the data type in the content list. Vertical separators are added between columns,
        and a horizontal separator is added after the headings.
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
        Activates the profile management interface by initializing and displaying the ProfileFrame.

        This method is bound to the profile button in the GUI. When the profile button is clicked, this method is called to switch the current view to the ProfileFrame, allowing the user to manage their profile settings.
        """
        ProfileFrame(self.container)

    def home_cmd(self):
        """
        Executes the home command which initializes and displays the main frame of the application.

        This method reinitializes the frames within the container and sets the "MainFrame" as the visible frame, effectively bringing the user to the home screen of the application.
        """
        self.container.init_frames()
        self.container.show_frame('MainFrame')

    def help_cmd(self, event=None):
        """
        Handles the help command by raising a NotImplementedError when invoked.

        This method is bound to the help button in the GUI. When the help button is clicked,
        this method is triggered but currently does not have an implementation, indicating
        that the functionality is yet to be developed or is intentionally left unimplemented.

        Parameters:
            event (optional): The event object that triggered this method. Defaults to None.
        """
        raise NotImplementedError

    def update_frame(self):
        """
        Updates the current frame in the GUI.

        This method is intended to be implemented in derived classes, where it will handle the specifics of updating the GUI frame based on the context and state of the application. As it stands, it raises a NotImplementedError, indicating that it should be overridden in subclasses.
        """
        raise NotImplementedError
