import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as font
from gui.containerframe import ContainerFrame
from gui.helperframes import ScaleHelpFrame, ImportHelpFrame
from core.fileinteraction import FileValidation
import pandas as pd


class ScaleFrame(ContainerFrame):
    """
    ScaleFrame is a class designed to manage and display a user interface for selecting scale types and weights in a data analysis application.

    This class provides methods to populate the frame with appropriate widgets based on the mode of operation, handle user interactions, and update the frame dynamically. It is derived from a superclass that provides the basic frame functionalities, likely a Tkinter Frame or a similar GUI component.

    Attributes:
        center_container (tkinter.Frame): The central container where widgets are placed.
        scale_types (list): A list of available scale types (nominal, ordinal, interval, ratio).
        selected_scale (str): The currently selected scale type.
        container (object): An object that holds the current mode and other relevant data for the frame.

    Methods:
        populate_frame(mode):
            Populate the frame with widgets based on the given mode.
        populate_weights():
            Populate the center container with widgets related to weight selection.
        populate_scaletype():
            Populate the center container with widgets related to selecting a scale type.
        next_cmd():
            Handle the action to be taken when the "Weiter" (Next) button is clicked.
        help_cmd(event=None):
            Display the help frame for the ScaleFrame.
        update_frame():
            Update the frame by clearing existing widgets and repopulating it based on the current mode.
    """

    def __init__(self, container):
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
        Populate the frame with widgets based on the given mode.

        Parameters:
            mode (str): The mode in which the frame should be populated. 
                        If 'analyse', both scale type and weights are populated.
                        Otherwise, only the scale type is populated.
        """
        if mode == 'analyse':
            self.populate_scaletype()
            self.populate_weights()
        else:
            self.populate_scaletype()

    def populate_weights(self):
        """
        Populate the center container with widgets related to weight selection.

        This method creates and arranges the widgets for selecting weights in the 
        center container of the ScaleFrame. It includes a label for weights, an 
        OptionMenu for selecting a weight, and several informational labels explaining 
        the different weight options.

        The method also configures the layout of these widgets within the center 
        container.

        Returns:
            None
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
        Populate the center container with widgets related to selecting a scale type.

        This method creates and places a label, an option menu for selecting a scale type, 
        and several informational labels describing different scale types (nominal, ordinal, 
        interval, and ratio) within the center container of the ScaleFrame. The available 
        scale types are provided in the `self.scale_types` list, and the selected scale type 
        is stored in the `self.selected_scale` variable.

        The layout of the widgets is managed using the grid and pack geometry managers.
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
                ""\"
                Handles the action to be taken when the "Weiter" (Next) button is clicked.

                This method updates the container's scale format and weights based on the user's selection.
                It then updates the "FileFrame" and displays it.

                If the container's mode is "analyse", it also updates the container's weights.
                ""\"
        """
        self.container.scale_format = self.selected_scale.get()
        if self.container.mode == 'analyse':
            self.container.weights = self.selected_weight.get()
        self.container.frames['FileFrame'].update_frame()
        self.container.show_frame('FileFrame')

    def help_cmd(self, event=None):
        """
        Display the help frame for the ScaleFrame.

        Parameters:
        event (tkinter.Event, optional): The event that triggered the help command. Defaults to None.
        """
        ScaleHelpFrame(self.container)

    def update_frame(self):
        """
        Update the frame by clearing existing widgets and repopulating it based on the current mode.

        This method removes all widgets from the `center_container` except for buttons and frames,
        and then repopulates the frame according to the mode specified in the container.

        Args:
            None

        Returns:
            None
        """
        for widget in self.center_container.winfo_children():
            if not isinstance(widget, tk.ttk.Button) and not isinstance(widget,
                tk.Frame):
                widget.destroy()
        self.populate_frame(self.container.mode)


class FileFrame(ContainerFrame):
    """
    FileFrame is a class designed to handle file selection, validation, and display within a Tkinter-based application. It provides functionalities to import files, validate their formats, and update the user interface accordingly. The class supports various file types including Excel (.xlsx, .xls), LibreOffice Calc (.ods), and CSV (.csv) files. It also includes a help command to assist users and a method to refresh the frame's content.

    Attributes:
        Inherits from a Tkinter Frame or similar superclass.

    Methods:
        - select_file(container): Opens a file dialog for the user to select a file, validates the file format, and updates the container with the file's data.
        - help_cmd(event=None): Displays the help frame for the ScaleFrame.
        - update_frame(): Clears existing widgets and repopulates the frame with the appropriate format preview.
    """

    def __init__(self, container):
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
        Selects a file for import and validates its format.

        Parameters:
            container (tk.Tk): The main application container.

        This method opens a file dialog for the user to select a file. It supports Excel (.xlsx, .xls), LibreOffice Calc (.ods), and CSV (.csv) files. Once a file is selected, it attempts to validate the file based on the current scale format. If the file is valid, it updates the container with the file's data and navigates to the appropriate frame based on the current mode (analyse or rate). If the file is invalid or an error occurs during import, an error message is displayed.
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
        Display the help frame for the ScaleFrame.

        Parameters:
        event (tkinter.Event, optional): The event that triggered the help command. Defaults to None.
        """
        ImportHelpFrame(self.container)

    def update_frame(self):
        """
        Update the frame by clearing existing widgets and repopulating it with the appropriate format preview.

        This method is used to refresh the frame, typically when the user navigates back to this frame. It ensures that any widgets from a previous session are removed and the frame is repopulated with the correct format preview based on the current settings.

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
