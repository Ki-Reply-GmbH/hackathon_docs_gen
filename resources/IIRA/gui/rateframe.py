import math
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from gui.containerframe import ContainerFrame
from gui.helperframes import RateHelpFrame
PROFILE = 0
RATING = 1


class RateFrame(ContainerFrame):
    """
    The RateFrame class is designed to facilitate the interactive rating of text entries within a graphical user interface (GUI). It provides comprehensive functionality for managing text data, categorizing entries, navigating through items, and handling user interactions such as text selection, category assignment, and data manipulation.

    This class integrates various components such as text display, navigation controls, category selection, and session management to offer a seamless rating experience. It supports operations like shuffling text entries, deleting categories or questions, saving sessions, and more. The class is structured to work within a larger application framework, typically receiving a container object that includes database and GUI configuration settings.

    Key functionalities include:
    - Displaying and navigating text entries.
    - Managing category inputs for ratings.
    - Handling user interactions through buttons, hotkeys, and entry fields.
    - Saving and deleting rating sessions.
    - Providing help and guidance on using the rating interface.
    """

    def __init__(self, container):
        """
            ""\"
            Initialize the RateFrame with a reference to the container that holds the database interaction and GUI configuration.

            Args:
            container (ContainerFrame): The parent container frame that holds the database interaction object and GUI styling configurations.
            ""\"
        """
        self.text = []
        self.text_index = 0
        self.profile = container.dbinteraction.active_profile
        self.ratings = []
        self.total_ratings = 0
        self.shuffler = None
        self.undo_shuffler = None
        super().__init__(container)
        container.style.configure('RateFrame.Treeview', font=
            'Arial 16 bold', rowheight=30)
        container.style.configure('RateFrame.Treeview.Heading', font='Arial 18'
            )
        container.style.configure('RateFrame.TRadiobutton', font='Arial 16')
        container.style.configure('Red.TLabel', foreground='#CC0000')
        container.style.configure('Orange.TLabel', foreground='#FF8000')
        container.style.configure('Yellow.TLabel', foreground='#CCCC00')
        container.style.configure('Lightgreen.TLabel', foreground='#00FF00')
        container.style.configure('Green.TLabel', foreground=self.accent_color)
        self.bind('<Right>', self.next_cmd)
        self.bind('<Left>', self.prev_cmd)
        left_frame = ttk.Frame(self)
        mid_frame = ttk.Frame(self)
        right_frame = ttk.Frame(self)
        top_frame = ttk.Frame(self)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(1, weight=1)
        separator_frame = ttk.Frame(self.menu_bar)
        separator_frame.grid(row=0, column=5, sticky='nsew')
        vert_separator = ttk.Separator(self.menu_bar, orient='vertical')
        vert_separator.grid(row=0, column=6, sticky='nsew')
        save_frame = ttk.Frame(self.menu_bar, width=75, height=50)
        save_label = ttk.Label(save_frame, text='Speichern', image=self.
            container.save_icon, compound='top', font='Arial 12')
        save_frame.bind('<Enter>', lambda x: self.on_enter(save_frame,
            save_label))
        save_frame.bind('<Leave>', lambda x: self.on_leave(save_frame,
            save_label))
        save_frame.bind('<Button-1>', lambda x: self.save_cmd())
        save_label.bind('<Button-1>', lambda x: self.save_cmd())
        save_frame.grid(row=0, column=7, sticky='nsew')
        save_label.place(relx=0.5, rely=0.5, anchor='center')
        delete_frame = ttk.Frame(self.menu_bar, width=85, height=50)
        delete_label = ttk.Label(delete_frame, text='Verwerfen', image=self
            .container.delete_icon, compound='top', font='Arial 12')
        delete_frame.bind('<Enter>', lambda x: self.on_enter(delete_frame,
            delete_label))
        delete_frame.bind('<Leave>', lambda x: self.on_leave(delete_frame,
            delete_label))
        delete_frame.bind('<Button-1>', lambda x: self.delete_cmd())
        delete_label.bind('<Button-1>', lambda x: self.delete_cmd())
        delete_frame.grid(row=0, column=8, sticky='nsew')
        delete_label.place(relx=0.5, rely=0.5, anchor='center')
        horizon_separator = ttk.Separator(self.menu_bar, orient='horizontal')
        horizon_separator.grid(row=1, column=6, columnspan=3, sticky='nsew')
        self.menu_bar.grid(row=0, column=0, columnspan=3, sticky='nsew')
        self.menu_bar.columnconfigure(5, weight=1)
        left_frame.grid(row=3, column=0, sticky='nsew')
        left_frame.rowconfigure(0, weight=1)
        columns = 'text'
        self.text_preview = ttk.Treeview(left_frame, columns=columns, show=
            'headings', style='RateFrame.Treeview', selectmode='browse')
        self.text_preview.heading('text', text='Navigation')
        self.text_preview.pack(fill='both', expand=True, pady=25, padx=5)
        self.text_preview.tag_configure('unselected', font='Arial 14')
        self.text_preview.bind('<Double-Button-1>', self.doubleclick_treeview)
        self.text_preview.bind('<Right>', self.next_cmd)
        self.text_preview.bind('<Left>', self.prev_cmd)
        self.percent_label = ttk.Label(top_frame, text='0 %', font=
            'Arial 20', style='Red.TLabel')
        self.percent_label.pack()
        top_frame.grid(row=2, column=1, sticky='nsew')
        self.text_label = ttk.Label(mid_frame, text='', font='Arial 20')
        mid_btn_container = ttk.Frame(mid_frame)
        prev_btn = ttk.Button(mid_btn_container, text='❮', command=self.
            prev_cmd)
        next_btn = ttk.Button(mid_btn_container, text='❯', command=self.
            next_cmd)
        prev_btn.pack(side='left', padx=5)
        next_btn.pack(side='right', padx=5)
        mid_frame.grid(row=3, column=1, sticky='nsew')
        self.text_label.grid(row=0, column=0)
        mid_btn_container.grid(row=1, column=0, pady=20)
        mid_frame.rowconfigure(0, weight=1)
        mid_frame.columnconfigure(0, weight=1)
        right_seperator0 = ttk.Frame(right_frame)
        right_seperator1 = ttk.Frame(right_frame)
        self.categories_var = tk.StringVar()
        right_frame.grid(row=3, column=2, sticky='nsew', padx=(5, 15), pady=10)
        self.rbtn_container = ttk.Frame(right_frame)
        right_seperator0.grid(row=1, column=0)
        self.rbtn_container.grid(row=2, column=0)
        right_seperator1.grid(row=3, column=0)
        right_frame.rowconfigure(1, weight=1)
        right_frame.rowconfigure(3, weight=1)
        self.populate_categories()

    def populate_navigation(self):
        """
            ""\"
            Populates the navigation treeview with parent and child nodes based on the text data.

            This method divides the text data into segments and creates a hierarchical view in the treeview widget.
            Each parent node represents a group of text entries, and each child node represents a single text entry.
            The method ensures that the first parent node and the first child node are expanded and focused upon initialization.
            ""\"
        """
        upper_limit = math.ceil(len(self.text) / 10)
        for i in range(upper_limit):
            if i == upper_limit - 1:
                self.text_preview.insert('', 'end', iid='parent_' + str(i),
                    open=False, values=('Elemente ' + str(i * 10 + 1) +
                    ' - ' + str(len(self.text)),))
            else:
                self.text_preview.insert('', 'end', iid='parent_' + str(i),
                    open=False, values=('Elemente ' + str(i * 10 + 1) +
                    ' - ' + str(i * 10 + 10),))
            for j in range(10):
                k = j + 10 * i
                if k >= len(self.text):
                    break
                n = self.count_upper_case(self.text[k], 18)
                nav_text = self.text[k]
                if len(self.text[k]) > n:
                    nav_text = self.text[k][:n] + '...'
                self.text_preview.insert('parent_' + str(i), 'end', iid=
                    'child_' + str(k), open=False, values=(nav_text,), tags
                    ='unselected')
        self.text_preview.item('parent_0', open=True)
        self.text_preview.focus('child_0')
        self.text_preview.selection_set('child_0')

    def randomize(self, mode):
        """
        Randomizes the order of text entries and their corresponding ratings based on the specified mode.

        This method can operate in two modes:
        - "do": Shuffles the text entries and their corresponding ratings randomly.
        - "undo": Restores the original order of text entries and their corresponding ratings using a previously stored state.

        Parameters:
            mode (str): The mode of operation, either "do" for shuffling or "undo" for restoring original order.
        """
        if mode == 'do':
            self.shuffler = np.random.permutation(len(self.text))
            self.undo_shuffler = np.argsort(self.shuffler)
            self.text = [self.text[j] for j in self.shuffler]
            self.ratings = [self.ratings[j] for j in self.shuffler]
        if mode == 'undo':
            self.text = [self.text[j] for j in self.undo_shuffler]
            self.ratings = [self.ratings[j] for j in self.undo_shuffler]

    def doubleclick_treeview(self, event):
        """
            ""\"
            Handles the double-click event on a treeview item in the text preview.

            This method identifies the treeview item that was double-clicked and updates the text display
            based on the selected item. It also updates the category selection if a rating already exists for the item.

            Parameters:
            - event: The event object containing details about the double-click action.

            The method updates the text index to reflect the selected item, populates the text display,
            and sets the category variable if a rating exists. It ensures the focus is set back to the widget
            after the operation.
            ""\"
        """
        item_iid = self.text_preview.identify_row(event.y)
        if 'child_' in item_iid:
            self.text_index = int(item_iid.replace('child_', ''))
            self.populate_text()
            if self.ratings[self.text_index] != ():
                self.categories_var.set(self.ratings[self.text_index][RATING])
            else:
                self.categories_var.set('')
        self.focus_set()

    def delete_questions(self):
        """
        Deletes all items from the text preview treeview within the RateFrame.

        This method clears the entire treeview used for displaying text elements by removing
        each child node. It is typically used to reset the view when needed.
        """
        for item in self.text_preview.get_children():
            self.text_preview.delete(item)

    def populate_categories(self):
        """
        Populates the category selection interface based on the scale format specified in the container.

        This method dynamically creates and displays the appropriate input widgets for category selection in the rating interface.
        If the scale format is 'intervall' or 'ratio', it sets up an entry field for numerical input. For other scale formats,
        it creates a series of radio buttons corresponding to the categories available in the container. Additionally, it binds
        numeric hotkeys to these categories for quick selection if the scale format is 'nominal' or 'ordinal'.
        """
        if (self.container.scale_format == 'intervall' or self.container.
            scale_format == 'ratio'):
            info_label = ttk.Label(self.rbtn_container, text='Eingegeben:',
                font='Arial 16')
            self.var_entered = ttk.Label(self.rbtn_container, text='n.a.',
                font='Arial 16')
            self.var_input = ttk.Entry(self.rbtn_container, textvariable=
                self.categories_var, text='Zahlenwert eingeben', font=
                'Arial 16')
            self.var_input.bind('<Return>', self.entry_input_cmd)
            info_label.pack(pady=5)
            self.var_entered.pack(pady=5)
            self.var_input.pack(pady=15)
        else:
            categories_rbtns = []
            for i in range(len(self.container.categories)):
                categories_rbtns.append(ttk.Radiobutton(self.rbtn_container,
                    text=self.container.categories[i], variable=self.
                    categories_var, value=self.container.categories[i],
                    style='RateFrame.TRadiobutton', command=self.label_text))
                categories_rbtns[i].pack(side='top', anchor='nw', pady=5)
                if i < 9:
                    if (self.container.scale_format == 'nominal' or self.
                        container.scale_format == 'ordinal'):
                        self.bind_all(str(i + 1), self.cat_hotkey_cmd)

    def delete_categories(self):
        """
            ""\"
            Removes all category-related widgets from the rating button container.

            This method iterates through all child widgets of the `rbtn_container` frame and destroys each one,
            effectively clearing all category selection options (e.g., radio buttons) from the GUI.
            ""\"
        """
        children_widgets = self.rbtn_container.winfo_children()
        for widget in children_widgets:
            widget.destroy()

    def populate_text(self):
        """
            ""\"
            Updates the text label in the GUI with the current text entry from the text list,
            formatted to include newlines for better readability.

            This method formats the current text entry to fit within the GUI's text display area,
            ensuring that the text is broken into lines that do not exceed a certain length,
            making it easier to read. It uses the `add_newlines` method to insert newlines at appropriate
            positions based on the length of the text and the presence of uppercase characters.
            ""\"
        """
        self.text_label.config(text=self.add_newlines(self.text[self.
            text_index], 75))

    def add_newlines(self, text, n):
        """
            ""\"
            Inserts newlines into the provided text to ensure that no line exceeds the specified length `n`.

            This method first adjusts the maximum line length `n` based on the number of uppercase characters in the text.
            It then attempts to break the text into lines that do not exceed this length, ideally breaking at space characters
            to avoid breaking words. If a word itself is longer than `n`, it is split with a newline character.

            Parameters:
                text (str): The text to be processed.
                n (int): The desired maximum number of characters per line.

            Returns:
                str: The processed text with newlines inserted to ensure that no line exceeds the length `n`.
            ""\"
        """
        n = self.count_upper_case(text, n)
        if len(text) < n:
            return text
        form_text = ''
        for word in text.split(' '):
            if len(word) > n:
                word = word[:n] + '\n' + word[n:]
            form_text += word + ' '
        offset = 0
        try:
            while True:
                p = form_text.rindex(' ', offset, offset + n)
                form_text = form_text[:p] + '\n' + form_text[p + 1:]
                offset = p
                if len(form_text[p + 1:]) < n:
                    return form_text
        except ValueError:
            pass
        return form_text

    def count_upper_case(self, text, n):
        """
            ""\"
            Adjusts the maximum length of text based on the count of uppercase characters.

            This method counts the number of uppercase characters in the provided text.
            If the count of uppercase characters is at least half the length of the text,
            it reduces the provided maximum length 'n' by 25%.

            Parameters:
                text (str): The text to analyze.
                n (int): The initial maximum length to consider.

            Returns:
                int: The adjusted maximum length based on the count of uppercase characters.
            ""\"
        """
        count_upper_case = 0
        for char in text:
            if char.isupper():
                count_upper_case += 1
        if count_upper_case >= len(text) // 2:
            n = int(n * 0.75)
        return n

    def entry_input_cmd(self, event=None):
        """
            ""\"
            Handles the input from the entry field for category ratings.

            This method is triggered when the user presses the 'Return' key in the entry field.
            It sets the category variable to the value entered, updates the ratings data structure,
            moves to the next rating item, and clears the entry field.

            Parameters:
                event (tk.Event, optional): The event that triggered this method. Defaults to None.
            ""\"
        """
        if len(self.var_input.get()) == 0:
            return
        self.categories_var.set(self.var_input.get())
        self.label_text()
        self.next_cmd()
        self.var_input.delete(0, 'end')

    def cat_hotkey_cmd(self, event):
        """
            ""\"
            Handles the keyboard shortcut input for category selection in the rating process.

            This method updates the category variable based on the number key pressed by the user.
            It adjusts the rating in the data structure and updates the navigation frame on the left side
            to reflect the selected category.

            Parameters:
            - event: The event object containing details of the key press.
            ""\"
        """
        category_no = int(event.char) - 1
        self.categories_var.set(self.container.categories[category_no])
        self.label_text()

    def next_cmd(self, event=None):
        """
            ""\"
            Advances to the next text item in the list, updates the display, and handles the navigation logic.

            This method is bound to the right arrow key and the next button. It updates the text index to the next item,
            updates the displayed text, and manages the navigation treeview to reflect the current position. If the end of
            the list is reached, it does nothing. It also handles the display of ratings if they exist for the new text item.

            Args:
                event: The event that triggered this method, default is None. This is used to handle event bindings.
            ""\"
        """
        self.focus_set()
        if self.text_index == len(self.text) - 1:
            return
        else:
            self.text_index = self.text_index + 1
            self.populate_text()
            if self.ratings[self.text_index] != ():
                self.categories_var.set(self.ratings[self.text_index][RATING])
                if (self.container.scale_format == 'intervall' or self.
                    container.scale_format == 'ratio'):
                    self.var_entered.config(text=self.categories_var.get())
            else:
                self.categories_var.set('')
                if (self.container.scale_format == 'intervall' or self.
                    container.scale_format == 'ratio'):
                    self.var_entered.config(text='n.a.')
            parent_iid = 'parent_' + str(self.text_index // 10)
            self.text_preview.item(parent_iid, open=True)
            for i in range(math.ceil(len(self.text) / 10)):
                other_parent_iid = 'parent_' + str(i)
                if other_parent_iid != parent_iid:
                    self.text_preview.item(other_parent_iid, open=False)
            child_iid = 'child_' + str(self.text_index)
            self.text_preview.focus(child_iid)
            self.text_preview.selection_set(child_iid)

    def prev_cmd(self, event=None):
        """
            ""\"
            Navigate to the previous text item in the list.

            This method decrements the text index to move to the previous item in the text list,
            updates the display to show the previous text, and adjusts the GUI components accordingly.
            If the current text index is at the start of the list, no action is taken.

            Args:
                event: An optional event parameter which is not used in the method.
            ""\"
        """
        self.focus_set()
        if self.text_index == 0:
            return
        else:
            self.text_index = self.text_index - 1
            self.populate_text()
            if self.ratings[self.text_index] != ():
                self.categories_var.set(self.ratings[self.text_index][RATING])
                if (self.container.scale_format == 'intervall' or self.
                    container.scale_format == 'ratio'):
                    self.var_entered.config(text=self.categories_var.get())
            else:
                self.categories_var.set('')
                if (self.container.scale_format == 'intervall' or self.
                    container.scale_format == 'ratio'):
                    self.var_entered.config(text='n.a.')
            parent_iid = 'parent_' + str(self.text_index // 10)
            self.text_preview.item(parent_iid, open=True)
            for i in range(math.ceil(len(self.text) / 10)):
                other_parent_iid = 'parent_' + str(i)
                if other_parent_iid != parent_iid:
                    self.text_preview.item(other_parent_iid, open=False)
            child_iid = 'child_' + str(self.text_index)
            self.text_preview.focus(child_iid)
            self.text_preview.selection_set(child_iid)

    def save_cmd(self):
        """
            ""\"
            Saves the current ratings to a file.

            This method first undoes any shuffling of text entries if shuffling was applied.
            It then prompts the user to choose a file name and file type (Excel, Libreoffice Calc, or CSV)
            and saves the ratings to the specified file using the file validation method from the container.
            ""\"
        """
        if self.shuffler is not None:
            self.randomize('undo')
        self.focus_set()
        filename = tk.filedialog.asksaveasfilename(filetypes=[(
            'Excel files', '.xlsx .xls'), ('Libreoffice Calc files', '.ods'
            ), ('Csv files', '.csv')])
        self.container.filevalidation.write_file(filename, self.ratings)

    def delete_cmd(self):
        """
            ""\"
            Handles the deletion of the entire rating session after confirmation from the user.

            This method prompts the user with a confirmation dialog asking if they want to discard
            the entire rating session. If the user confirms, it resets the ratings, clears the
            category variable, and updates the frame to reflect these changes.
            ""\"
        """
        self.focus_set()
        result = messagebox.askyesno(title='Verwerfen', message=
            'Die gesamte Bewertungssession verwerfen?')
        if result:
            self.categories_var.set('')
            self.ratings = []
            for text_entry in self.text:
                self.ratings.append(())
                self.text_index = 0
                self.update_frame()
        else:
            return

    def label_text(self, event=None):
        """
            ""\"
            Handles the labeling of text elements based on the selected category from the radio buttons or entry field.
            Updates the internal ratings list, the navigation treeview, and the percentage of labeled items.

            This method is triggered when a category is selected or changed in the GUI. It updates the ratings for the
            current text element, modifies the navigation treeview to reflect the labeling status, and updates the
            percentage of completed labels displayed on the GUI.

            Args:
                event: An optional event parameter that can be used to trigger this method from a GUI event.
            ""\"
        """
        self.focus_set()
        if self.ratings[self.text_index]:
            if self.ratings[self.text_index][RATING
                ] == self.categories_var.get():
                self.ratings[self.text_index] = ()
                self.categories_var.set('')
                self.total_ratings -= 1
                self.populate_percentage()
                child_iid = 'child_' + str(self.text_index)
                self.text_preview.item(child_iid, tags=self.text_preview.
                    item(child_iid, 'tags')[0])
                self.text_preview.item(child_iid, values=(self.text_preview
                    .item(child_iid, 'values')[0].replace(' ✓', ''),))
                parent_iid = self.text_preview.parent(child_iid)
                values = self.text_preview.item(parent_iid, 'values')
                values = values[0].replace('     ✓', ''),
                self.text_preview.item(parent_iid, values=values)
            else:
                self.ratings[self.text_index] = (self.container.
                    dbinteraction.active_profile, self.categories_var.get())
        else:
            self.ratings[self.text_index] = (self.container.dbinteraction.
                active_profile, self.categories_var.get())
            self.total_ratings += 1
            self.populate_percentage()
            child_iid = 'child_' + str(self.text_index)
            tags = self.text_preview.item(child_iid, 'tags')
            values = self.text_preview.item(child_iid, 'values')
            if 'labeled' not in tags:
                tags += 'labeled',
                values = values[0] + ' ✓',
            self.text_preview.item(child_iid, tags=tags)
            self.text_preview.item(child_iid, values=values)
            self.text_preview.selection_set(child_iid)
            parent_iid = self.text_preview.parent(child_iid)
            for child_iid in self.text_preview.get_children(parent_iid):
                tags = self.text_preview.item(child_iid, 'tags')
                if 'labeled' not in tags:
                    return
            values = self.text_preview.item(parent_iid, 'values')
            values = values[0] + '     ✓',
            self.text_preview.item(parent_iid, values=values)
            self.update()
            self.labeling_finished()

    def labeling_finished(self):
        """
            ""\"
            Check if all text elements have been rated and prompt the user to save the ratings.

            This method checks if the total number of ratings matches the number of text elements.
            If all elements have been rated, it prompts the user with a message asking if they
            want to save the ratings. If the user agrees, it triggers the save command.
            ""\"
        """
        if self.total_ratings == len(self.text):
            result = messagebox.askyesno(title='Glückwunsch', message=
                """Du hast alle Textelemente bewertet.
Bewertungen speichern?"""
                )
            if result:
                self.save_cmd()

    def populate_percentage(self):
        """
            ""\"
            Updates the percentage of rated text elements and adjusts the style of the percentage label based on the completion rate.

            This method calculates the percentage of text elements that have been rated and updates the text of the percentage label.
            It also changes the style of the label to reflect different levels of completion using color coding:
            - Red for less than 20% completion
            - Orange for 20% to 39% completion
            - Yellow for 40% to 59% completion
            - Light green for 60% to 79% completion
            - Green for 80% to 100% completion
            ""\"
        """
        percentage = int(100 * self.total_ratings / len(self.text))
        percentage_str = str(int(100 * self.total_ratings / len(self.text))
            ) + ' %'
        self.percent_label.config(text=percentage_str)
        if percentage < 20:
            self.percent_label.config(style='Red.TLabel')
        elif percentage < 40:
            self.percent_label.config(style='Orange.TLabel')
        elif percentage < 60:
            self.percent_label.config(style='Yellow.TLabel')
        elif percentage < 80:
            self.percent_label.config(style='Lightgreen.TLabel')
        else:
            self.percent_label.config(style='Green.TLabel')

    def home_cmd(self):
        """
        Navigate the user back to the main frame and optionally save the current session.

        This method prompts the user with a dialog asking if they want to save the current rating session.
        If the user chooses to save, the `save_cmd` method is called to handle the saving process.
        Afterwards, or if the user chooses not to save, the method initializes the main frames and displays the main frame.

        Returns:
            None
        """
        result = messagebox.askyesno(title='Speichern?', message=
            'Soll die Bewertungssession gespeichert werden?')
        if result:
            self.save_cmd()
        self.container.init_frames()
        self.container.show_frame('MainFrame')

    def help_cmd(self, event=None):
        """
            ""\"
            Opens the help frame for the RateFrame.

            This method triggers the display of the RateHelpFrame which provides
            help and guidance on how to use the rating interface.

            Args:
                event: An optional event parameter that can be passed if the method
                       is triggered by an event. Defaults to None.
            ""\"
        """
        RateHelpFrame(self.container)

    def update_frame(self, mode=None):
        """
            ""\"
            Updates the frame by setting up the text, ratings, categories, and navigation based on the current state.

            This method is responsible for initializing or updating the text display, ratings, and navigation elements
            within the frame. It can also handle randomization of the text order if specified.

            Args:
                mode (str, optional): If set to "do", the text will be randomized. Defaults to None.
            ""\"
        """
        self.focus_set()
        self.text = self.container.formatted_text
        for text_entry in self.text:
            self.ratings.append(())
        if mode == 'do':
            self.randomize(mode)
        self.delete_categories()
        self.populate_categories()
        self.delete_questions()
        self.populate_navigation()
        self.populate_text()
        self.populate_percentage()
