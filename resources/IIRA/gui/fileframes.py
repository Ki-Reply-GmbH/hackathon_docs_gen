import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as font
from gui.containerframe import ContainerFrame
from gui.helperframes import ScaleHelpFrame, ImportHelpFrame
from core.fileinteraction import FileValidation
import pandas as pd


class ScaleFrame(ContainerFrame):
    """
    The ScaleFrame class is designed to be a versatile user interface component within a larger application, 
    typically for data analysis purposes. It facilitates user interaction for selecting scale types and weights 
    appropriate for their data analysis needs. The class provides dynamic configuration of its content based 
    on different operational modes, such as 'analyse', and integrates functionalities to update and navigate 
    through the application states.

    This class manages the layout and behavior of widgets related to scale type and weight selection, 
    including the initialization within a specified container, dynamic population of widgets based on the 
    selected mode, and updating the frame as needed. It also includes methods for advancing the application 
    state and providing help related to the available options.
    """

    def __init__(self, container):
        """
            ""\"
            Initialize the ScaleFrame with a specified container.

            This method sets up the ScaleFrame within the given container, configuring the necessary styles,
            variables, and layout for scale and weight selection interfaces. It also initializes the navigation
            and display components within the frame.

            Args:
            container (ttk.Frame): The parent container in which this frame will be placed.
            ""\"
        """
        super().__init__(container)
        self.scale_types = ['nominal', 'ordinal', 'intervall', 'ratio']
        self.weights = ['identity', 'linear', 'quadratic', 'bipolar',
            'circular', 'ordinal', 'radial', 'ratio']
        self.selected_scale = tk.StringVar()
        self.selected_weight = tk.StringVar()
        container.style.configure('FileFrame.TMenubutton', font='Arial 18',
            foreground='black', width=10)
        self.center_container = ttk.Frame(self, style='Card', padding=(5, 6,
            7, 8))
        next_button = ttk.Button(self.center_container, text='Weiter',
            style='FileFrame.TButton', command=self.next_cmd)
        self.menu_bar.grid(row=0, column=0, columnspan=2, sticky='nsew')
        self.center_container.grid(row=1, column=0, sticky='nsew', padx=15,
            pady=15)
        tk.Frame(self.center_container).grid(row=3, column=0, columnspan=3)
        next_button.grid(row=4, column=0, columnspan=3)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.center_container.columnconfigure(0, weight=1)
        self.center_container.rowconfigure(0, weight=1)
        self.center_container.rowconfigure(1, weight=1)
        self.center_container.rowconfigure(2, weight=1)
        self.center_container.rowconfigure(3, weight=1)

    def populate_frame(self, mode):
        """
        Populates the frame with appropriate widgets based on the specified mode.

        This method configures the frame's content dynamically depending on the mode provided.
        If the mode is 'analyse', it populates both scale types and weights. For other modes,
        it only populates the scale types.

        Parameters:
            mode (str): The mode of operation which determines the widgets to be displayed.
                        Expected values are 'analyse' or other specific modes.
        """
        if mode == 'analyse':
            self.populate_scaletype()
            self.populate_weights()
        else:
            self.populate_scaletype()

    def populate_weights(self):
        """
        Populates the weight selection interface in the GUI.

        This method sets up the labels, dropdown menu, and information labels related to the weight options
        within the center container of the ScaleFrame. It configures the layout and ensures that the weight
        selection components are displayed correctly, providing users with options to choose how categories
        are weighted in their analysis.
        """
        weights_label = ttk.Label(self.center_container, font='Arial 22',
            text='Gewichte')
        weights_menu = ttk.OptionMenu(self.center_container, self.
            selected_weight, 'identity', *self.weights, style=
            'FileFrame.TMenubutton')
        infolabel_container = ttk.Frame(self.center_container)
        weights_infolabel = ttk.Label(infolabel_container, font='Arial 18',
            text=
            '• Legen fest in welchem Verhältnis die Kategorien zueinander stehen.'
            )
        identity_infolabel = ttk.Label(infolabel_container, font='Arial 18',
            text=
            """• Identity entspricht den ungewichteten Metriken.
  Übereinstimmung nur dann, wenn exakt die gleiche
  Kategorie ausgewählt wurde. """
            )
        linear_infolabel = ttk.Label(infolabel_container, font='Arial 18',
            text='• Üblich sind die Gewichte identity, linear, oder quadratic.'
            )
        weights_label.grid(row=0, column=1, pady=10)
        weights_menu.grid(row=1, column=1, pady=20)
        infolabel_container.grid(row=2, column=1, pady=10)
        weights_infolabel.pack(fill='x', pady=5)
        identity_infolabel.pack(fill='x', pady=5)
        linear_infolabel.pack(fill='x', pady=5)
        self.center_container.columnconfigure(0, weight=1)

    def populate_scaletype(self):
        """
            ""\"
            Populates the scale type selection interface within the center container of the ScaleFrame.

            This method sets up labels and an option menu for selecting the scale type, and provides
            informational labels about each scale type. The scale types include nominal, ordinal,
            interval, and ratio scales, each described with their characteristics to aid the user
            in making an appropriate selection based on their data analysis needs.
            ""\"
        """
        scale_format_label = ttk.Label(self.center_container, font=
            'Arial 22', text='Skalenformat')
        scale_menu = ttk.OptionMenu(self.center_container, self.
            selected_scale, 'nominal', *self.scale_types, style=
            'FileFrame.TMenubutton')
        infolabel_container = ttk.Frame(self.center_container)
        nominal_infolabel = ttk.Label(infolabel_container, font='Arial 18',
            text='• Nominalskala: Objekte werden nur mit Namen versehen.')
        ordinal_infolabel = ttk.Label(infolabel_container, font='Arial 18',
            text=
            """• Ordinalskala: Es gibt zusätzlich eine Äquivalenz- und
  Ordungsrelation."""
            )
        intervall_infolabel = ttk.Label(infolabel_container, font=
            'Arial 18', text=
            '• Intervallskala: Zusätzlich sind Abstände/Intervall definierbar.'
            )
        rational_infolabel = ttk.Label(infolabel_container, font='Arial 18',
            text='• Rationalskala: Es gibt zusätzlich einen Nullpunkt.')
        scale_format_label.grid(row=0, column=0, pady=10)
        scale_menu.grid(row=1, column=0, pady=20)
        infolabel_container.grid(row=2, column=0, pady=10)
        nominal_infolabel.pack(fill='x', pady=5)
        ordinal_infolabel.pack(fill='x', pady=5)
        intervall_infolabel.pack(fill='x', pady=5)
        rational_infolabel.pack(fill='x', pady=5)
        self.center_container.columnconfigure(0, weight=1)

    def next_cmd(self):
        """
        Advances the application state by setting the selected scale format and weight, and then transitions to the "FileFrame".

        This method retrieves the selected scale format and, if the mode is "analyse", also retrieves the selected weight. It then updates the "FileFrame" based on these selections and displays it.
        """
        self.container.scale_format = self.selected_scale.get()
        if self.container.mode == 'analyse':
            self.container.weights = self.selected_weight.get()
        self.container.frames['FileFrame'].update_frame()
        self.container.show_frame('FileFrame')

    def help_cmd(self, event=None):
        """
        Opens a help dialog specific to the ScaleFrame, providing guidance on scale types and weight options.
        """
        ScaleHelpFrame(self.container)

    def update_frame(self):
        """
        Updates the frame by clearing existing widgets and repopulating based on the current mode.
        This method is responsible for refreshing the visual components of the frame whenever
        the underlying data or state changes, ensuring that the display is consistent with the
        current application context.
        """
        for widget in self.center_container.winfo_children():
            if not isinstance(widget, tk.ttk.Button) and not isinstance(widget,
                tk.Frame):
                widget.destroy()
        self.populate_frame(self.container.mode)


class FileFrame(ContainerFrame):
    """
    The FileFrame class is designed to manage and interact with file data within a graphical user interface. It provides functionalities to initialize a frame within a container, select files from the file system, populate previews of data formats, and update the frame based on user interactions or data changes. This class is essential for applications that require data import, format validation, and dynamic display updates based on the selected data format and application mode. It also includes a help command to assist users with scale types and weight options, enhancing user experience and usability.
    """

    def __init__(self, container):
        """
            ""\"
            Initialize the ScaleFrame with a specified container.

            This method sets up the ScaleFrame within the given container, configuring the necessary styles,
            variables, and layout for scale and weight selection interfaces. It also initializes the navigation
            and display components within the frame.

            Args:
            container (ttk.Frame): The parent container in which this frame will be placed.
            ""\"
        """
        super().__init__(container)
        container.style.configure('FileFrame.TButton', font='Arial 18',
            foreground='black')
        center_container = ttk.Frame(self, style='Card', padding=(5, 6, 7, 8))
        file_import_label = ttk.Label(center_container, font='Arial 20',
            text='Datei importieren')
        accepted_formats_label = ttk.Label(center_container, font=
            'Arial 20', text='Es werden zwei Formate akzeptiert')
        format_1_label = ttk.Label(center_container, font='Arial 20', text=
            'Format 1:')
        self.format_1_container = ttk.Frame(center_container)
        self.format_1_bulletlist_container = ttk.Frame(center_container)
        format_2_label = ttk.Label(center_container, font='Arial 20', text=
            'Format 2:')
        self.format_2_container = ttk.Frame(center_container)
        self.format_2_bulletlist_container = ttk.Frame(center_container)
        self.format_1_2_bulletlist_container = ttk.Frame(center_container)
        select_file_button = ttk.Button(center_container, text=
            'Datei auswählen', style='FileFrame.TButton', command=lambda :
            self.select_file(container))
        center_container.grid(row=1, column=0, sticky='nsew', padx=15, pady=15)
        self.menu_bar.grid(row=0, column=0, columnspan=2, sticky='nsew')
        file_import_label.grid(row=0, column=0, columnspan=3, pady=10)
        accepted_formats_label.grid(row=1, column=0, columnspan=3, pady=10)
        format_1_label.grid(row=2, column=0, pady=15)
        format_2_label.grid(row=2, column=2, pady=15)
        self.format_1_container.grid(row=3, column=0, padx=15)
        ttk.Frame(center_container).grid(row=2, rowspan=2, column=1, sticky
            ='nsew')
        self.format_2_container.grid(row=3, column=2, padx=15)
        self.format_1_bulletlist_container.grid(row=4, column=0, padx=15,
            pady=(15, 0))
        self.format_2_bulletlist_container.grid(row=4, column=2, padx=15,
            pady=(15, 0))
        self.format_1_2_bulletlist_container.grid(row=5, column=0, columnspan=3
            )
        ttk.Frame(center_container).grid(row=6, column=0, columnspan=3)
        select_file_button.grid(row=7, column=0, columnspan=3)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        center_container.columnconfigure(1, weight=1)
        center_container.rowconfigure(6, weight=1)

    def populate_format_preview(self, format_container):
        """
            ""\"
            Populates the specified format container with a preview of data format based on the selected scale format.

            This method dynamically generates a preview of how data should be formatted in the file to be imported,
            depending on whether the scale format is nominal, ordinal, or other types (like interval or ratio).
            It adjusts the displayed information and table structure in the GUI to guide the user in preparing their data files correctly.

            Args:
            format_container (ttk.Frame): The container frame where the format preview will be displayed.

            The method checks the current scale format and populates the appropriate format container with example data,
            headers, and informational labels that explain the requirements for each data format.
            ""\"
        """
        if (self.container.scale_format == 'nominal' or self.container.
            scale_format == 'ordinal'):
            if format_container == self.format_1_container:
                headings = ['Categories', 'Rater ID',
                    'Sentiment Analysis\nis nice!',
                    """If I run the code in
the GUI, it just hangs."""]
                content = [['positive', 'Alice', 'positive', 'neutral'], [
                    'neutral', 'Bob', 'positive', 'negative'], ['negative']]
                self.create_table(self.format_1_container, headings, content)
                rater_id_infolabel = ttk.Label(self.
                    format_1_bulletlist_container, font='Arial 18', text=
                    '• Header "Rater ID" muss in Datei vorkommen.')
                rater_id_infolabel.pack(fill='x', pady=5)
            else:
                headings = ['Categories', 'Subject', 'Alice', 'Bob']
                content = [['positive', 'Sentiment Analysis\nis nice!',
                    'positive', 'positive'], ['neutral',
                    """If I run the code in
the GUI, it just hangs.""",
                    'neutral', 'negative'], ['negative']]
                self.create_table(self.format_2_container, headings, content)
                text_infolabel = ttk.Label(self.
                    format_2_bulletlist_container, font='Arial 18', text=
                    '• Header "Subject" muss in Datei vorkommen.')
                text_infolabel.pack(fill='x', pady=5)
                categories_infolabel = ttk.Label(self.
                    format_1_2_bulletlist_container, font='Arial 18', text=
                    '• Header "Categories" in beiden Formaten.')
                if self.container.scale_format == 'nominal':
                    info_txt = (
                        '• Kategorienamen angeben; hier: positive, neutral, negative.'
                        )
                else:
                    info_txt = """• Kategorienamen in sortierter Reihenfolge angeben.
  (aufsteigend, oder absteigend)"""
                category_entries_infolabel = ttk.Label(self.
                    format_1_2_bulletlist_container, font='Arial 18', text=
                    info_txt)
                black_headers_infolabel = ttk.Label(self.
                    format_1_2_bulletlist_container, font='Arial 18', text=
                    '• Spalten mit schwarzen Header werden automatisch erkannt.'
                    )
                other_columns_infolabel = ttk.Label(self.
                    format_1_2_bulletlist_container, font='Arial 18', text=
                    '• Andere Spalten werden ignoriert.')
                categories_infolabel.pack(fill='x', pady=5)
                category_entries_infolabel.pack(fill='x', pady=5)
                black_headers_infolabel.pack(fill='x', pady=5)
                other_columns_infolabel.pack(fill='x', pady=5)
        elif format_container == self.format_1_container:
            headings = ['Rater ID', 'Herzfrequenz\n24.01. 16:30',
                'Herzfrequenz\n24.01. 17:00']
            content = [['Alice', '121.5', '89'], ['Bob', '123', '75']]
            self.create_table(self.format_1_container, headings, content)
            rater_id_infolabel = ttk.Label(self.
                format_1_bulletlist_container, font='Arial 18', text=
                '• Header "Rater ID" muss in Datei vorkommen.')
            rater_id_infolabel.pack(fill='x', pady=15)
        else:
            headings = ['Subject', 'Alice', 'Bob']
            content = [['Herzfrequenz\n24.01. 16:30', '121.5', '123'], [
                """Herzfrequenz
24.01. 17:00""", '89', '75']]
            self.create_table(self.format_2_container, headings, content)
            text_infolabel = ttk.Label(self.format_2_bulletlist_container,
                font='Arial 18', text=
                '• Header "Subject" muss in Datei vorkommen.')
            text_infolabel.pack(fill='x', pady=15)
            other_columns_infolabel = ttk.Label(self.
                format_1_2_bulletlist_container, font='Arial 18', text=
                '• Spalten die davor auftauchen werden ignoriert.')
            subjects_infolabel = ttk.Label(self.
                format_1_2_bulletlist_container, font='Arial 18', text=
                '• Danach ausschließlich Spalten mit den Messergebnissen.')
            other_columns_infolabel.pack(fill='x', pady=15)
            subjects_infolabel.pack(fill='x', pady=15)

    def select_file(self, container):
        """
        Opens a file dialog for the user to select a file, and processes the selected file based on the current application mode.

        This method allows the user to select a file from their file system with specific file types (.xlsx, .xls, .ods, .csv).
        After a file is selected, it validates and processes the file according to the scale format specified in the container.
        If the file is valid, it updates the application state and transitions to the appropriate frame based on the mode ('analyse' or 'rate').

        Parameters:
            container (ContainerFrame): The container frame that holds the application state and manages transitions between frames.

        Raises:
            messagebox: If the file import fails, an error message is displayed to the user.
        """
        filename = tk.filedialog.askopenfilename(filetypes=[('Excel files',
            '.xlsx .xls'), ('Libreoffice Calc files', '.ods'), ('Csv files',
            '.csv')])
        if filename == '':
            return
        try:
            container.filevalidation = FileValidation(filename, self.
                container.scale_format)
            container.categories = container.filevalidation.categories
            container.rater_ids = container.filevalidation.rater_ids
            container.text = container.filevalidation.text
            container.formatted_text = container.filevalidation.formatted_text
            container.labels = container.filevalidation.labels
        except:
            messagebox.showerror(title='Error', message=
                'Fehler beim importieren der Datei. Auf passendes Format geachtet?'
                )
            return
        if container.mode == 'analyse':
            container.frames['AnalyseFrame'].update_frame()
            container.show_frame('AnalyseFrame')
        elif container.mode == 'rate':
            result = messagebox.askyesno(title='Reihenfolge', message=
                'Soll die Reihenfolge der Bewertungsobjekte zufällig sein?')
            if result:
                container.frames['RateFrame'].update_frame(mode='do')
            else:
                container.frames['RateFrame'].update_frame()
            container.show_frame('RateFrame')
        else:
            container.show_frame('MainFrame')

    def help_cmd(self, event=None):
        """
        Opens a help dialog specific to the ScaleFrame, providing guidance on scale types and weight options.
        """
        ImportHelpFrame(self.container)

    def update_frame(self):
        """
        Updates the frame by clearing existing widgets and repopulating based on the current mode.
        This method is responsible for refreshing the visual components of the frame whenever
        the underlying data or state changes, ensuring that the display is consistent with the
        current application context.
        """
        for widget in self.format_1_container.winfo_children():
            widget.destroy()
        for widget in self.format_2_container.winfo_children():
            widget.destroy()
        for widget in self.format_1_bulletlist_container.winfo_children():
            widget.destroy()
        for widget in self.format_2_bulletlist_container.winfo_children():
            widget.destroy()
        for widget in self.format_1_2_bulletlist_container.winfo_children():
            widget.destroy()
        self.populate_format_preview(self.format_1_container)
        self.populate_format_preview(self.format_2_container)
