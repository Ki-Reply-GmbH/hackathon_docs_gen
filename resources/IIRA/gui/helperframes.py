import tkinter as tk
from tkinter import ttk, messagebox
import shutil
import platform
import os
import webbrowser
file_path = os.path.dirname(os.path.realpath(__file__))
urls = [
    'https://irrcac.readthedocs.io/en/latest/irrCAC.html#module-irrCAC.weights'
    , 'https://journals.sagepub.com/doi/pdf/10.1177/001316446002000104',
    'https://psycnet.apa.org/record/1980-29309-001',
    'https://psycnet.apa.org/record/1972-05083-001',
    'https://www.narcis.nl/publication/RecordID/oai:repository.ubn.ru.nl:2066%2F54804'
    ,
    'https://bpspsychub.onlinelibrary.wiley.com/doi/abs/10.1348/000711006X126600'
    , 'https://agreestat.com/papers/wiley_encyclopedia2008_eoct631.pdf']


class ProfileFrame(tk.Toplevel):
    """
    ProfileFrame is a class designed to manage user profiles within a graphical user interface (GUI) application. It provides functionalities to create, change, and delete user profiles, as well as to update the profile-related UI elements.

    Attributes:
        - profile_name_label: A label widget that displays the name of the currently active profile.
        - change_profile_mbutton: A menu button widget that allows users to switch between different profiles.
        - dbinteraction: An object that handles interactions with the database, including retrieving and updating profile information.

    Methods:
        - create_new_profile: Creates a new profile input field if it does not already exist.
        - change_profile: Changes the active user profile to the selected profile.
        - delete_profile: Deletes the currently active profile if there are multiple profiles available.
        - ok_cmd: Handles the 'Ok' button command to create a new profile or close the window.
        - populate_profile_label: Updates the profile name label with the active profile name from the database.
        - populate_change_profile_menu: Populates the change profile menu with the list of available profiles.

    This class is typically derived from a GUI framework class, such as a Frame in Tkinter, to provide a structured and interactive interface for managing user profiles.
    """

    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.user_input = tk.StringVar(value='')
        self.title('Profil')
        self.geometry('500x300')
        self.resizable(False, False)
        container_frame = ttk.Frame(self)
        signed_in_as_label = ttk.Label(container_frame, text=
            'Angemeldet als', font='Arial 18')
        self.profile_name_label = ttk.Label(container_frame, text=self.
            container.dbinteraction.active_profile, font='Arial 18', image=
            self.container.face_icon, compound='left')
        self.separator_frame = ttk.Frame(container_frame)
        create_delete_container = ttk.Frame(container_frame)
        button_container = ttk.Frame(container_frame)
        create_profile_button = ttk.Button(create_delete_container, text=
            'Profil anlegen', command=self.create_new_profile)
        delete_profile_button = ttk.Button(create_delete_container, text=
            'Profil löschen', command=self.delete_profile)
        ok_button = ttk.Button(button_container, text='Ok', style=
            'Accent.TButton', command=self.ok_cmd)
        self.change_profile_mbutton = ttk.Menubutton(button_container, text
            ='Profil wechseln')
        change_profile_menu = tk.Menu(self.change_profile_mbutton, tearoff=
            False)
        self.change_profile_mbutton.configure(menu=change_profile_menu)
        profile_selection = tk.StringVar()
        for user in self.container.dbinteraction.profiles:
            change_profile_menu.add_radiobutton(variable=profile_selection,
                value=user, label=user, command=lambda : self.
                change_profile(profile_selection.get()))
        container_frame.pack(fill='both', expand=True)
        signed_in_as_label.grid(row=0, column=0, padx=15, pady=15)
        self.profile_name_label.grid(row=1, column=0, columnspan=2, padx=15,
            pady=15)
        self.separator_frame.grid(row=2, column=0, columnspan=2)
        create_delete_container.grid(row=3, column=0, rowspan=2, padx=15,
            pady=15)
        button_container.grid(row=4, column=1, columnspan=2)
        self.change_profile_mbutton.grid(row=0, column=1, padx=15, pady=15)
        ok_button.grid(row=0, column=2, padx=15, pady=15)
        create_profile_button.pack(side='top', pady=5)
        delete_profile_button.pack(side='bottom', pady=5)
        container_frame.rowconfigure(2, weight=1)

    def ok_cmd(self, event=None):
        """
        Handles the 'Ok' button command. If the user input is empty, the window is closed without creating a new profile. 
        If the user input is not empty, a new profile is created with the provided name, and the profile-related UI elements 
        are updated accordingly.

        Args:
            event (optional): The event that triggered the command. Default is None.
        """
        if len(self.user_input.get()) == 0:
            self.destroy()
        else:
            self.container.dbinteraction.create_profile(self.user_input.get())
            self.populate_profile_label()
            self.populate_change_profile_menu()
            self.user_input.set('')
            for widget in self.separator_frame.winfo_children():
                widget.destroy()

    def populate_profile_label(self):
        """
        Update the profile name label with the active profile name from the database interaction.

        This method configures the `profile_name_label` to display the currently active profile name
        retrieved from the `dbinteraction` attribute of the container.

        Returns:
            None
        """
        self.profile_name_label.configure(text=self.container.dbinteraction
            .active_profile)

    def populate_change_profile_menu(self):
        """
        Populate the change profile menu with the list of available profiles.

        This method updates the menu associated with the `change_profile_mbutton` to include
        all profiles stored in the `dbinteraction` object of the container. Each profile is 
        added as a radio button, allowing the user to select and switch to a different profile.

        The method performs the following steps:
        1. Creates a new `tk.Menu` object and assigns it to the `change_profile_mbutton`.
        2. Initializes a `StringVar` to keep track of the selected profile.
        3. Iterates over the list of profiles from `dbinteraction.profiles`.
        4. Adds each profile as a radio button to the menu, setting the command to change the profile.

        This method ensures that the profile menu is always up-to-date with the current list of profiles.

        Returns:
            None
        """
        change_profile_menu = tk.Menu(self.change_profile_mbutton, tearoff=
            False)
        self.change_profile_mbutton.configure(menu=change_profile_menu)
        profile_selection = tk.StringVar()
        for user in self.container.dbinteraction.profiles:
            change_profile_menu.add_radiobutton(variable=profile_selection,
                value=user, label=user, command=lambda : self.
                change_profile(profile_selection.get()))

    def create_new_profile(self):
        """
        Create a new profile input field if it does not already exist.

        This method checks if the input field for creating a new profile is already present.
        If it is not, it adds a label and an entry widget to the separator frame, allowing
        the user to input the name of the new profile. The entry widget is also bound to the
        Return key to trigger the `ok_cmd` method when the user presses Enter.

        Returns:
            None
        """
        if not self.separator_frame.winfo_children():
            name_label = ttk.Label(self.separator_frame, text='Name:', font
                ='Arial 16')
            name_label.pack(side='left', padx=15)
            input = ttk.Entry(self.separator_frame, textvariable=self.
                user_input)
            input.bind('<Return>', self.ok_cmd)
            input.pack(side='right')

    def change_profile(self, profile_selection):
        """
        Change the active user profile to the selected profile.

        Args:
            profile_selection (str): The name of the profile to switch to.

        This method updates the active profile in the database interaction layer,
        refreshes the profile name label, and repopulates the profile selection menu.
        """
        self.container.dbinteraction.change_profile(profile_selection)
        self.populate_profile_label()
        self.populate_change_profile_menu()

    def delete_profile(self):
        """
        Deletes the currently active profile if there are multiple profiles available. 
        If the active profile is the only profile, an error message is displayed prompting 
        the user to create a new profile before deleting the current one.
        """
        if len(self.container.dbinteraction.profiles) == 0:
            messagebox.showerror(title='Einziges Profil', message=
                'Das ist dein einziges Profil. Erstelle erst ein Neues, um es zu löschen.'
                )
        else:
            self.container.dbinteraction.delete_profile()
            self.populate_profile_label()
            self.populate_change_profile_menu()


class ScrollFrame(ttk.Frame):
    """
    ScrollFrame is a custom widget that provides a scrollable frame within a Tkinter canvas.

    This class is designed to handle various events related to scrolling and resizing, ensuring that the content within the frame can be navigated smoothly using mouse wheel events and that the scroll region is updated appropriately when the size of the frame or canvas changes.

    Attributes:
        - Inherits from a Tkinter widget class (e.g., Frame, Canvas).

    Methods:
        - onFrameConfigure(event): Updates the scroll region of the canvas whenever the size of the viewPort frame changes.
        - onCanvasConfigure(event): Handles the configuration event for the canvas, adjusting the width of the canvas window to match the new width of the canvas.
        - onMouseWheel(event): Handles mouse wheel events for scrolling the canvas, with behavior varying based on the operating system.
        - onEnter(event): Binds mouse wheel events to the canvas when the cursor enters the control, with bindings specific to the operating system.
        - onLeave(event): Unbinds the mouse wheel events from the canvas when the cursor leaves the control.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.vsb = ttk.Scrollbar(self, orient='vertical')
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
            yscrollcommand=self.vsb.set, background='#ffffff')
        self.viewPort = ttk.Frame(self.canvas)
        self.vsb.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.canvas_window = self.canvas.create_window((4, 4), window=self.
            viewPort, anchor='nw', tags='self.viewPort')
        self.viewPort.bind('<Configure>', self.onFrameConfigure)
        self.canvas.bind('<Configure>', self.onCanvasConfigure)
        self.viewPort.bind('<Enter>', self.onEnter)
        self.viewPort.bind('<Leave>', self.onLeave)
        self.onFrameConfigure(None)

    def onFrameConfigure(self, event):
        """
        Update the scroll region of the canvas whenever the size of the viewPort frame changes.

        Args:
            event (tkinter.Event): The event that triggered this method, typically a <Configure> event.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def onCanvasConfigure(self, event):
        """
        Handle the configuration event for the canvas.

        This method is called whenever the size of the canvas changes. It adjusts the width of the canvas window to match the new width of the canvas.

        Args:
            event (tk.Event): The event object containing information about the canvas configuration event.
        """
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def onMouseWheel(self, event):
        """
        Handle mouse wheel events for scrolling the canvas.

        Args:
            event (tkinter.Event): The event object containing information about the mouse wheel event.

        Behavior:
            - On Windows, scrolls the canvas vertically based on the event delta divided by 120.
            - On macOS (Darwin), scrolls the canvas vertically based on the event delta.
            - On other platforms (e.g., Linux), scrolls the canvas vertically based on the event number (4 for up, 5 for down).
        """
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), 'units')
        elif event.num == 4:
            self.canvas.yview_scroll(-1, 'units')
        elif event.num == 5:
            self.canvas.yview_scroll(1, 'units')

    def onEnter(self, event):
        """
        Bind mouse wheel events to the canvas when the cursor enters the control.

        Args:
            event (tk.Event): The event object containing information about the event.

        Binds the appropriate mouse wheel events to the canvas based on the operating system.
        For Linux, it binds the Button-4 and Button-5 events. For other systems, it binds the MouseWheel event.
        """
        if platform.system() == 'Linux':
            self.canvas.bind_all('<Button-4>', self.onMouseWheel)
            self.canvas.bind_all('<Button-5>', self.onMouseWheel)
        else:
            self.canvas.bind_all('<MouseWheel>', self.onMouseWheel)

    def onLeave(self, event):
        """
        Unbinds the mouse wheel events from the canvas when the cursor leaves the control.

        Args:
            event: The event object containing information about the leave event.
        """
        if platform.system() == 'Linux':
            self.canvas.unbind_all('<Button-4>')
            self.canvas.unbind_all('<Button-5>')
        else:
            self.canvas.unbind_all('<MouseWheel>')


class MainHelpFrame(tk.Toplevel):
    """
    MainHelpFrame is a class that initializes a help window with tabs and help text for different sections of the application.

    Attributes:
        container (tk.Tk or tk.Toplevel): The parent container for this Toplevel window.

    This class is derived from a superclass that provides the necessary functionality to create a Toplevel window in a Tkinter application.
    """

    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.title('Hilfe - Hauptmenü')
        self.geometry('500x650')
        self.notebook = ttk.Notebook(self)
        tab_general = ttk.Frame(self.notebook)
        tab_analyse = ttk.Frame(self.notebook)
        tab_rate = ttk.Frame(self.notebook)
        self.notebook.add(tab_general, text='Generell')
        self.notebook.add(tab_analyse, text='Analysieren')
        self.notebook.add(tab_rate, text='Bewerten')
        self.notebook.pack(expand=True, fill='both')
        general_txt = tk.Text(tab_general, foreground='black', background=
            'white', relief='flat', font='Arial 18', highlightthickness=0,
            borderwidth=0)
        general_txt.insert('end',
            """Das Hilfe-Symbol gibt dir auf jeder Seite Hinweise zu den Funktionalitäten der App.

"""
            )
        general_txt.insert('end',
            """Auf jeder Seite werden unterschiedliche Hilfsvorschläge angezeigt, je nachdem welche Elemente gerade in der App angezeigt werden.

"""
            )
        general_txt.insert('end',
            'Die Navigation erfolgt über die Tabs. Jeder Tab beinhaltet nähere Informationen zu den wichtigsten Elementen, die dir in der App begegnen werden.'
            )
        general_txt.pack(padx=15, pady=30)
        analyse_txt = tk.Text(tab_analyse, foreground='black', background=
            'white', relief='flat', font='Arial 18', highlightthickness=0,
            borderwidth=0)
        analyse_txt.insert('end',
            """Die Analysieren-Funktion ermöglicht es dir Intra-, und
Inter-Rater-Reliability-Untersuchungen durchzuführen.

"""
            )
        analyse_txt.insert('end',
            """Folgende Metriken können verwendet werden, um die
Reliability-Untersuchungen vorzunehmen:

"""
            )
        analyse_txt.insert('end',
            """• Cohen's κ
• Conger's κ• Fleiss' κ
• Krippendorff's α
• Gwet's AC
• ICC

"""
            )
        analyse_txt.insert('end',
            """Die für die Reliability-Untersuchungen benötigten Daten
werden im nächsten Schritt abgefragt."""
            )
        analyse_txt.pack(padx=15, pady=30)
        rate_txt = tk.Text(tab_rate, foreground='black', background='white',
            relief='flat', font='Arial 18', highlightthickness=0, borderwidth=0
            )
        rate_txt.insert('end',
            """Die Bewerten-Funktion ermöglicht es dir einen Datensatz zu importieren der von dir, oder einem
anderen SW-Nutzer, bewertet werden soll.

"""
            )
        rate_txt.insert('end',
            """Dabei können die Daten mit beliebigen Labeln versehen werden (Kategorisierung).

"""
            )
        rate_txt.insert('end',
            """Alternativ ist es möglich den Daten kontinuierliche Werte zuzuordnen, wie es beispielsweise beim Messen von
Sehstärken der Fall wäre."""
            )
        rate_txt.pack(padx=15, pady=30)


class ScaleHelpFrame(tk.Toplevel):
    """
    ScaleHelpFrame is a class that manages the user interface for handling profile creation and updates.

    This class is responsible for handling user interactions, specifically the 'Ok' button click event, to create new profiles based on user input. It updates the profile label and change profile menu accordingly and manages the widgets in the separator frame.

    Attributes:
        Inherits from a superclass or implements an interface (not specified in the provided context).
    """

    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.title('Hilfe - Skalen & Gewichte')
        self.geometry('500x650')
        self.notebook = ttk.Notebook(self)
        tab_scale = ttk.Frame(self.notebook)
        tab_weights = ttk.Frame(self.notebook)
        self.notebook.add(tab_scale, text='Skalenformate')
        self.notebook.add(tab_weights, text='Gewichte')
        self.notebook.pack(expand=True, fill='both')
        scale_txt = tk.Text(tab_scale, foreground='black', background=
            'white', relief='flat', font='Arial 18', highlightthickness=0,
            borderwidth=0)
        scale_txt.tag_configure('bold', font='Arial 18 bold')
        scale_txt.insert('end',
            """Das Skalenformat beschreibt Eigenschaften der zu betrachtenden Daten. Man kann zwischen den folgenden Skalenformaten
untescheiden:

"""
            )
        scale_txt.insert('end', 'Nominalskala:\n ', 'bold')
        scale_txt.insert('end',
            """• Klassifikationen und Kategorisierungen
sind möglich
• Objekte stehen nicht notwendigerweise
  in Relation zueinander
• z.B. {"Rot", "Haus", "Stadt"}

"""
            )
        scale_txt.insert('end', 'Ordinalskala:\n', 'bold')
        scale_txt.insert('end',
            """• Es gibt zusätzlich eine Äquivalenzrelation
x = y
• Und eine Ordnungsrelation x < y
• z.B. Schulnoten

"""
            )
        scale_txt.insert('end', 'Intervallskala:\n', 'bold')
        scale_txt.insert('end',
            """• Abstände (Intervalle) sind definiert
• z.B. (01.01.22 -> 03.01.22)
        = (01.01.23 -> 03.01.23)
• Rechnen mit Intervallen ist erlaubt,
mit Werten nicht

"""
            )
        scale_txt.insert('end', 'Rationalskala:\n', 'bold')
        scale_txt.insert('end',
            """• Die Skala hat zusätzlich einen Nullpunkt
• Es darf mit den Werten multipliziert
  und dividiert werden.
• Dadurch könnn Verhältnisse gebildet werden.
• z.B. Programm A ist doppelt so schnell
  wie Programm B."""
            )
        scale_txt.pack(padx=15, pady=30)
        weights_txt = """Warum sind Gewichte erorderlich?

Wenn man beispielsweise das ungewichtete Cohen's κ betrachtet und den Grad an Übereinstimmung messen möchte, so würden nur die Fälle als Übereinstimmung gewertet werden, bei denen beide Räter die gleiche Kategorie auswählen.


Gewichte ermöglich es darüber hinaus Beziehungen zwischen den Kategorien herzustellen.
So liegt es nahe, dass ein Rater der einen Text als positiv bewertet mit seiner Einschätzung mehr mit einem Rater übereinstimmt, der den selben Text als neutral bewertet, statt mit einem Rater, der ihn als negativ bewertet.

"""
        weights_txt = tk.Text(tab_weights, foreground='black', background=
            'white', relief='flat', font='Arial 18', highlightthickness=0,
            borderwidth=0)
        weights_txt.tag_configure('bold', font='Arial 18 bold')
        weights_txt.tag_configure('link', foreground='#217346', underline=True)
        weights_txt.tag_configure('0')
        weights_txt.tag_bind('0', '<Button-1>', lambda x: callback(urls[0]))
        weights_txt.insert('end', 'Warum sind Gewichte erorderlich?\n\n',
            'bold')
        weights_txt.insert('end',
            """Wenn man beispielsweise das ungewichtete Cohen's κ betrachtet und den Grad an Übereinstimmung messen möchte, so würden nur die Fälle als Übereinstimmung gewertet werden, bei denen beide Räter die gleiche Kategorie auswählen.

"""
            )
        weights_txt.insert('end',
            """Gewichte ermöglich es darüber hinaus Beziehungen zwischen den Kategorien herzustellen. So liegt es nahe, dass ein Rater der einen Text als positiv bewertet mit seiner Einschätzung mehr mit einem Rater übereinstimmt, der den selben Text als neutral bewertet, statt mit einem Rater, der ihn als negativ bewertet. Wie stark diese Beziehungen ausgeprägt sind, bzw. wie stark sie gewichtet werden sollen hängt von der Wahl des Gewichts ab.

"""
            )
        weights_txt.insert('end', 'Wie werden die Gewichte berechnet?\n\n',
            'bold')
        img = tk.PhotoImage(file=os.path.join(file_path,
            '../data/img/weights_identity.png'))
        weights_txt.insert('end',
            'Ausführliche Informationen zur Berechnung der Gewichte gibt es auf '
            )
        weights_txt.insert('end', 'dieser Website', ('link', '0'))
        weights_txt.insert('end', '.')
        weights_txt.pack(padx=15, pady=30)


class ImportHelpFrame(tk.Toplevel):
    """
    ImportHelpFrame is a class that provides help information for importing data in different formats.

    Attributes:
        notebook (ttk.Notebook): The notebook widget containing tabs for different import formats.

    Args:
        container: The parent container for this frame.
    """

    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.title('Hilfe - Importieren')
        self.geometry('500x650')
        self.notebook = ttk.Notebook(self)
        tab_format1 = ttk.Frame(self.notebook)
        tab_format2 = ttk.Frame(self.notebook)
        self.notebook.add(tab_format1, text='Format 1')
        self.notebook.add(tab_format2, text='Format 2')
        self.notebook.pack(expand=True, fill='both')
        format1_txt = tk.Text(tab_format1, foreground='black', background=
            'white', relief='flat', font='Arial 18', highlightthickness=0,
            borderwidth=0)
        format1_txt.tag_configure('bold', font='Arial 18 bold')
        format1_txt.insert('end', 'Format 1\n\n', 'bold')
        format1_txt.insert('end',
            """Beim ersten Format sind die Rater ID's in einer eigenen Spalte organisiert.  Es ist verpflichtend einem Header den Namen 'Rater ID' zu geben, damit die ID's gefunden werden können. Auf Groß- und Kleinschreibung wird beim Header nicht geachtet. Es ist aber darauf zu achten, dass der Headername nicht mehrfach vorkommt. Es darf die gleiche Rater ID mehrfach in der Spalte vorkommen. Mehrfache Vorkommnisse werden intern in dieser App zusammengefasst.


"""
            )
        format1_txt.insert('end', 'Diskretes Skalenformat\n\n', 'bold')
        format1_txt.insert('end',
            """Falls du ein diskretes Skalenformaten (nominal, ordinal) ausgewählt hast, muss die Datei zusätzlich eine Spalte mit dem Headernamen 'Categories' enthalten Die Spalte enthält alle Kategorienamen, die bei der Analyse, oder beim Bewerten, vorkommenkönnen. Die Kategorienamen sind case sensitive.
Es spielt keine Rolle wo die 'Rater ID'-, bzw. die 'Categories'-Spalten in der Datei auftauchen. Die Suche nach den Spalten erfolgt alleine durch den Namen.


"""
            )
        format1_txt.insert('end', 'Kontinuierliche Skalenformat\n\n', 'bold')
        format1_txt.insert('end',
            "Bei kontinuierlichen Skalenformaten (intervall, rational) gibt es keine 'Categories'-Spalte. Vor der 'Rater ID'-Spalte können beliebige Spalten auftauchen, die von IIRA ignoriert werden. Es ist wichtig, dass nach der 'Rater ID'-Spalte ausschließlich Spalten auftauchen, die die Bewertungen enthalten. Bei kontinuierlichen Skalenformaten können diese Spalten nämlich nicht durch die Kategorienamen automatisch gesucht werden."
            )
        format1_txt.pack(padx=15, pady=30)
        format2_txt = tk.Text(tab_format2, foreground='black', background=
            'white', relief='flat', font='Arial 18', highlightthickness=0,
            borderwidth=0)
        format2_txt.tag_configure('bold', font='Arial 18 bold')
        format2_txt.insert('end', 'Format 2\n\n', 'bold')
        format2_txt.insert('end',
            """Beim zweiten Format sind die Subjects in einer eigenen Spalte organisiert.  Es ist verpflichtend einem Header den Namen 'Subject' zu geben, damit die Subjects gefunden werden können. Auf Groß- und Kleinschreibung wird beim Header nicht geachtet. Es ist aber darauf zu achten, dass der Headername nicht mehrfach vorkommt. Es darf das gleiche Subject mehrfach in der Spalte vorkommen. Mehrfache Vorkommnisse werden intern in dieser App zusammengefasst.


"""
            )
        format2_txt.insert('end', 'Diskretes Skalenformat\n\n', 'bold')
        format2_txt.insert('end',
            """Falls du ein diskretes Skalenformaten (nominal, ordinal) ausgewählt hast, muss die Datei zusätzlich eine Spalte mit dem Headernamen 'Categories' enthalten Die Spalte enthält alle Kategorienamen, die bei der Analyse, oder beim Bewerten, vorkommenkönnen. Die Kategorienamen sind case sensitive.
Es spielt keine Rolle wo die 'Subject'-, bzw. die 'Categories'-Spalten in der Datei auftauchen. Die Suche nach den Spalten erfolgt alleine durch den Namen.


"""
            )
        format2_txt.insert('end', 'Kontinuierliche Skalenformat\n\n', 'bold')
        format2_txt.insert('end',
            "Bei kontinuierlichen Skalenformaten (intervall, rational) gibt es keine 'Categories'-Spalte. Vor der 'Subject'-Spalte können beliebige Spalten auftauchen, die von IIRA ignoriert werden. Es ist wichtig, dass nach der 'Subject'-Spalte ausschließlich Spalten auftauchen, die die Bewertungen enthalten. Bei kontinuierlichen Skalenformaten können diese Spalten nämlich nicht durch die Kategorienamen automatisch gesucht werden."
            )
        format2_txt.pack(padx=15, pady=30)


class PrepAnalyseHelpFrame(tk.Toplevel):
    """
    Provides help information for preparing analysis in the application.

    This class is designed to assist users in understanding how to prepare their data for analysis by providing detailed help content organized into tabs. It is derived from a superclass that manages the graphical user interface components.

    Attributes:
        container (tk.Tk): The parent container for this frame.
        notebook (ttk.Notebook): A notebook widget to organize help content into tabs.
        tab_rater (ttk.Frame): A tab containing information about selecting raters.
        tab_metrics (ttk.Frame): A tab containing information about selecting metrics.
        rater_txt (tk.Text): A text widget containing detailed information about rater selection.
        metrics_txt (tk.Text): A text widget containing detailed information about metric selection.
    """

    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.title('Hilfe - Analyse vorbereiten')
        self.geometry('500x650')
        self.notebook = ttk.Notebook(self)
        tab_rater = ttk.Frame(self.notebook)
        tab_metrics = ttk.Frame(self.notebook)
        self.notebook.add(tab_rater, text='Bewerter')
        self.notebook.add(tab_metrics, text='Metriken')
        self.notebook.pack(expand=True, fill='both')
        rater_txt = tk.Text(tab_rater, foreground='black', background=
            'white', relief='flat', font='Arial 18', highlightthickness=0,
            borderwidth=0)
        rater_txt.tag_configure('bold', font='Arial 18 bold')
        rater_txt.insert('end', 'Auswahl der Bewerter\n\n\n', 'bold')
        rater_txt.insert('end',
            """Durch die Auswahl der Bewerter wird festgelegt, von welchen Bewertern die Reliabilitätsuntersuchungen vorgenommen werden sollen.

Für jeden ausgewählten Intrarater wird eine eigene Intrarater-Reliabilitätsuntersuchung für den Bewerter vorgenommen.

Bei der Auswahl mehrerer Interrater, wird eine Interrater-Reliabilitätsuntersuchung für alle ausgewählten Bewerter erstellt."""
            )
        rater_txt.pack(padx=15, pady=30)
        metrics_txt = tk.Text(tab_metrics, foreground='black', background=
            'white', relief='flat', font='Arial 18', highlightthickness=0,
            borderwidth=0)
        metrics_txt.tag_configure('bold', font='Arial 18 bold')
        metrics_txt.tag_configure('link', foreground='#217346', underline=True)
        metrics_txt.tag_configure('1')
        metrics_txt.tag_bind('1', '<Button-1>', lambda x: callback(urls[1]))
        metrics_txt.tag_bind('2', '<Button-1>', lambda x: callback(urls[2]))
        metrics_txt.tag_bind('3', '<Button-1>', lambda x: callback(urls[3]))
        metrics_txt.tag_bind('4', '<Button-1>', lambda x: callback(urls[4]))
        metrics_txt.tag_bind('5', '<Button-1>', lambda x: callback(urls[5]))
        metrics_txt.tag_bind('6', '<Button-1>', lambda x: callback(urls[6]))
        metrics_txt.insert('end', 'Auswahl der Metriken\n\n', 'bold')
        metrics_txt.insert('end',
            """Durch die Auswahl der Metriken kann festgelegt werden, welche Metrikwerte für die  Reliabilitätsuntersuchungen berechnet werden sollen.

Weiterführende Informationen zu den Metriken, findest du unter den folgenden Links:

"""
            )
        metrics_txt.insert('end', "Cohen's κ\n", 'bold')
        metrics_txt.insert('end',
            """COHEN, Jacob. A coefficient of agreement for nominal scales. Educational and psychological measurement, 1960, 20. Jg., Nr. 1, S. 37-46.

"""
            , ('link', '1'))
        metrics_txt.insert('end', "Conger's κ\n", 'bold')
        metrics_txt.insert('end',
            """Anthony J Conger. Integration and generalization of kappas for multiple raters. Psychological Bulletin, 88(2):322, 1980.

"""
            , ('link', '2'))
        metrics_txt.insert('end', "Fleiss' κ\n", 'bold')
        metrics_txt.insert('end',
            """Joseph L Fleiss. Measuring nominal scale agreement among many raters. Psychological bulletin, 76(5):378, 1971.

"""
            , ('link', '3'))
        metrics_txt.insert('end', "Krippendorff's α\n", 'bold')
        metrics_txt.insert('end',
            """K. Krippendorff. Content Analysis: An Introduction To Its Methodology. Sage, Beverly Hills, CA, 1980.

"""
            , ('link', '4'))
        metrics_txt.insert('end', "Gwet's AC\n", 'bold')
        metrics_txt.insert('end',
            """GWET, Kilem Li. Computing inter‐rater reliability and its variance in the presence of high agreement. British Journal of Mathematical and Statistical Psychology, 2008, 61. Jg., Nr. 1, S. 29-48.

"""
            , ('link', '5'))
        metrics_txt.insert('end', 'ICC\n', 'bold')
        metrics_txt.insert('end',
            """GWET, Kilem L. Intrarater reliability. Wiley encyclopedia of clinical trials, 2008, 4. Jg.

"""
            , ('link', '6'))
        metrics_txt.pack(padx=15, pady=30)


class ResultsHelpFrame(tk.Toplevel):
    """
    Die Klasse stellt dem SW-User ein Hilsdialog zur Verfügung, in Abhängigkeit
    von dem Frame in dem sich der SW-User aktuell befindet.
    TODO
    """

    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.title('Hilfe - Ergebnisse')
        self.geometry('500x650')
        self.notebook = ttk.Notebook(self)
        tab_general = ttk.Frame(self.notebook)
        tab_interpratation = ttk.Frame(self.notebook)
        self.notebook.add(tab_general, text='Generell')
        self.notebook.add(tab_interpratation, text='Interpretation')
        self.notebook.pack(expand=True, fill='both')
        general_txt = tk.Text(tab_general, foreground='black', background=
            'white', relief='flat', font='Arial 18', highlightthickness=0,
            borderwidth=0)
        general_txt.tag_configure('bold', font='Arial 18 bold')
        general_txt.insert('end', 'Informationen zu den Ergebnissen\n\n',
            'bold')
        general_txt.insert('end',
            """Die Ergebnisse der Reliabilitätsuntersuchungen werden in zwei Tabs dargestellt. In einem Tab werden die Ergebnisse der Intrarater-Analyse dargestellt und im anderen Tab die Ergebnisse der Interrater-Analyse.
Vorausgesetzt, du hast im vorherigen Fenster die Auswahl getroffen, die entsprechenden Analysen vorzunehmen.

"""
            )
        general_txt.insert('end', 'ID\n', 'bold')
        general_txt.insert('end',
            """Die Spalte gibt an auf welche Bewerter-ID sich die Analyse bezieht.

"""
            )
        general_txt.insert('end', 'Metrikwerte\n', 'bold')
        general_txt.insert('end',
            """In den mittleren Spalten werden die Ergebnisse der Reliabilitätsuntersuchungen für jede ausgewählte Metrik angezeigt.

"""
            )
        general_txt.insert('end', '#Subjects\n', 'bold')
        general_txt.insert('end',
            """Die Spalte gibt an, wie viele Subjects, oder Bewertungsobjekte, es in der Reliabilitätsuntersuchung gibt.Falls ein Bewerter 10 unterschiedliche Subjects an zwei unterschiedlichen Beobachtungszeitpunkten bewertet hat, würde in der Spalte also eine 10 stehen.

"""
            )
        general_txt.insert('end', '#Replicates\n', 'bold')
        general_txt.insert('end',
            """Die Spalte gibt an, wie viele Replikate es gibt. Beim oberen Beispiel, in dem ein Bewerter 10 Subjects an zwei unterschiedlichen Beobachtungszeitpunkten bewertet hat, würde in der Spalte also eine 2 stehen.

"""
            )
        general_txt.insert('end', '#Rater\n', 'bold')
        general_txt.insert('end',
            'Bei der Interrater-Analyse wird zusätzlich in einer Spalte angegeben, wie viele Bewerter in der Analyse betrachtet worden sind.'
            )
        general_txt.pack(padx=15, pady=30)
        interpretation_txt = tk.Text(tab_interpratation, foreground='black',
            background='white', relief='flat', font='Arial 18',
            highlightthickness=0, borderwidth=0)
        interpretation_txt.tag_configure('bold', font='Arial 18 bold')
        interpretation_txt.insert('end',
            'Wie werden die Werte interpretiert?\n\n', 'bold')
        interpretation_txt.insert('end',
            """In der folgenden Tabelle wurde die gängige Interpretation der Ergebnisse der Intra- und Interrater-Analysen dargestellt. Die Interpretationsmöglichkeit gilt für alle auswählbaren Metriken.

"""
            )
        interpretation_txt.insert('end',
            'Interpretation nach Landis & Koch:\n\n', 'bold')
        interpretation_txt.insert('end',
            'Metrikwert | Grad der Übereinstimmung\n', 'bold')
        interpretation_txt.insert('end', '<0.00         | Poor\n')
        interpretation_txt.insert('end', '0.00 - 0.20 | Slight\n')
        interpretation_txt.insert('end', '0.21 - 0.40 | Fair\n')
        interpretation_txt.insert('end', '0.41 - 0.60 | Moderate\n')
        interpretation_txt.insert('end', '0.61 - 0.80 | Substantial\n')
        interpretation_txt.insert('end', '0.81 - 1.00 | Almost Perfect\n')
        interpretation_txt.pack(padx=15, pady=30)


class RateHelpFrame(tk.Toplevel):
    """
    Die Klasse stellt dem SW-User ein Hilsdialog zur Verfügung, in Abhängigkeit
    von dem Frame in dem sich der SW-User aktuell befindet.
    TODO
    """

    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.title('Hilfe - Bewerten')
        self.geometry('500x650')
        self.notebook = ttk.Notebook(self)
        tab_general = ttk.Frame(self.notebook)
        self.notebook.add(tab_general, text='Generell')
        self.notebook.pack(expand=True, fill='both')
        general_txt = tk.Text(tab_general, foreground='black', background=
            'white', relief='flat', font='Arial 18', highlightthickness=0,
            borderwidth=0)
        general_txt.tag_configure('bold', font='Arial 18 bold')
        general_txt.insert('end', 'Informationen zum Bewerten\n\n', 'bold')
        general_txt.insert('end',
            """In dieser Ansicht können die zuvor importierten Daten bewertet werden.

Es ist möglich über den Profil-Button das aktuelle Nutzerprofil zu wechseln. Die Bewertungen werden immer dem Profil zugeordnet, das gerade angemeldet ist. So ist es möglich während einer Bewertungssession mit unterschiedlichen Profilen Bewertungen vorzunehmen.

"""
            )
        general_txt.insert('end', 'Navigation\n', 'bold')
        general_txt.insert('end',
            """Das Navigations-Widget links ermöglicht es schnell zwischen den Fragen hin und her zu springen. Außerdem bietet es, neben der Statusbar oben, eine Übersicht darüber, wie viele Elemente bereits bewertet worden sind.
Zusätzlich sind die linke, bzw. die rechte, Pfeiltaste mit Hotkeys belegt, um zum vorherigen, bzw. zum nächsten, Element zu wechseln.

"""
            )
        general_txt.insert('end', 'Bewerten\n', 'bold')
        general_txt.insert('end',
            """Um eine Bewertung vorzunehmen, kannst du die Radiobuttons ganz links drücken.Die ersten 9 Kategorien sind zusätzlich mit den Hotkeys 1-9 belegt.
Bei kontinuierlichen Daten kann das Eingabefeld ganz links zum Bewerten genutzt werden.

"""
            )
        general_txt.insert('end', 'Speichern & Verwerfen\n', 'bold')
        general_txt.insert('end',
            """Zum Speichern, oder zum Verwerfen der aktuellen Bewertungssession sind die jeweiligen Buttons oben rechts zu drücken.

"""
            )
        general_txt.pack(padx=15, pady=30)


def callback(url):
    """ Die Funktion erhält ein String-Argument, welches im Webbrowser geöffnet wird. """
    webbrowser.open_new(url)
