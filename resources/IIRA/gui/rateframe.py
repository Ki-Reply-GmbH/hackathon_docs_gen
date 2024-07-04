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
    RateFrame Class

    The RateFrame class is a GUI component designed for managing and displaying text elements that need to be rated. It provides functionalities for navigating through text items, rating them, and saving the ratings. The class is derived from a Tkinter Frame and includes various methods to handle user interactions, update the display, and manage the rating process.

    Attributes:
        container (tk.Tk): The main container or parent widget for this frame.
        text (list): A list of text elements to be rated.
        ratings (list): A list to store the ratings for each text element.
        text_index (int): The current index of the text element being displayed.
        categories_var (tk.StringVar): A Tkinter variable to store the selected category.
        rbtn_container (tk.Frame): A frame to hold category-related widgets.
        text_label (tk.Label): A label to display the current text element.
        percentage_label (tk.Label): A label to display the rating progress percentage.

    Methods:
        __init__(self, container): Initialize the RateFrame class.
        populate_navigation(self): Populate the navigation tree view with parent and child nodes based on the text elements.
        randomize(self, mode): Randomizes the order of text and ratings or undoes the randomization.
        doubleclick_treeview(self, event): Handle double-click events on the Treeview widget.
        delete_questions(self): Delete all questions from the text preview tree view.
        populate_categories(self): Populate the categories section of the RateFrame based on the scale format.
        delete_categories(self): Delete all category-related widgets from the right button container.
        populate_text(self): Update the text label with the current text entry, formatted with newlines.
        add_newlines(self, text, n): Add newlines to a given text at specified intervals.
        count_upper_case(self, text, n): Count the number of uppercase characters in a given text and adjust the limit `n` based on the proportion of uppercase characters.
        entry_input_cmd(self, event): Handles the event when the user inputs a value in the entry field and presses the Return key.
        cat_hotkey_cmd(self, event): Handles the event when a category hotkey is pressed.
        next_cmd(self, event): Advance to the next text item in the list and update the display accordingly.
        prev_cmd(self, event): Navigate to the previous text item in the list and update the display accordingly.
        save_cmd(self): Save the current ratings to a file.
        delete_cmd(self): Prompt the user to confirm if they want to discard the entire rating session.
        label_text(self, event): Updates the rating for the current text element based on the selected category.
        labeling_finished(self): Check if all text elements have been rated and prompt the user to save the ratings if completed.
        populate_percentage(self): Update the percentage label to reflect the current progress of ratings.
        home_cmd(self): Prompt the user to save the current rating session and navigate back to the main frame.
        help_cmd(self, event): Display the help frame for the RateFrame.
        update_frame(self, mode): Update the frame with the current text and ratings, and optionally randomize the text order.
    """

    def __init__(self, container):
        """
        Initialize the RateFrame class.

        This method sets up the initial state of the RateFrame instance, including configuring styles, 
        binding events, and creating and arranging various GUI components such as frames, labels, buttons, 
        and tree views. It also initializes several instance variables related to text, ratings, and shuffling.

        Args:
            container (tk.Tk): The main container or parent widget for this frame.
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
        Populate the navigation tree view with parent and child nodes based on the text elements.

        The method divides the text elements into groups of 10 and creates parent nodes for each group.
        Each parent node contains child nodes representing individual text elements. The method also
        truncates long text elements and appends ellipses if necessary.

        The first parent node and its first child node are expanded and selected by default.

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
        Randomizes the order of text and ratings or undoes the randomization.

        Parameters:
            mode (str): The mode of operation. If "do", the text and ratings are randomized.
                        If "undo", the text and ratings are restored to their original order.
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
        Handle double-click events on the Treeview widget.

        This method is triggered when a user double-clicks on an item in the Treeview.
        It updates the current text index to the selected item, populates the text
        label with the corresponding text, and sets the category variable based on the
        existing rating for the selected text.

        Args:
            event (tkinter.Event): The event object containing information about the
            double-click event.
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
        Delete all questions from the text preview tree view.

        This method iterates through all the items in the text preview tree view and deletes them.
        """
        for item in self.text_preview.get_children():
            self.text_preview.delete(item)

    def populate_categories(self):
        """
        Populate the categories section of the RateFrame based on the scale format.

        If the scale format is "intervall" or "ratio", it creates an entry field for numerical input.
        Otherwise, it creates radio buttons for each category and binds hotkeys for quick selection.

        This method dynamically updates the user interface to reflect the appropriate input method for the current scale format.

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
        Delete all category-related widgets from the right button container.

        This method removes all widgets (e.g., radio buttons, labels, entry fields) 
        that are currently present in the right button container (`self.rbtn_container`).
        It is typically used to clear the existing category selection interface before 
        populating it with new categories or when resetting the interface.
        """
        children_widgets = self.rbtn_container.winfo_children()
        for widget in children_widgets:
            widget.destroy()

    def populate_text(self):
        """
        Update the text label with the current text entry, formatted with newlines.

        This method updates the `text_label` widget to display the current text entry from the `text` list, 
        formatted with newlines to ensure it fits within a specified width. The text entry to be displayed 
        is determined by the `text_index` attribute.

        Returns:
            None
        """
        self.text_label.config(text=self.add_newlines(self.text[self.
            text_index], 75))

    def add_newlines(self, text, n):
        """
        Add newlines to a given text at specified intervals.

        This method processes the input text and inserts newline characters at appropriate
        positions to ensure that no line exceeds a specified length. It also takes into account
        the presence of uppercase characters, adjusting the maximum line length accordingly.

        Args:
            text (str): The input text to be formatted.
            n (int): The maximum number of characters per line before inserting a newline.

        Returns:
            str: The formatted text with newline characters inserted.
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
        Count the number of uppercase characters in a given text and adjust the limit `n` based on the proportion of uppercase characters.

        Args:
            text (str): The text in which to count uppercase characters.
            n (int): The initial limit to be adjusted based on the count of uppercase characters.

        Returns:
            int: The adjusted limit `n`. If the number of uppercase characters is at least half the length of the text, the limit `n` is reduced to 75% of its original value.
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
        Handles the event when the user inputs a value in the entry field and presses the Return key.

        Parameters:
        event (tkinter.Event, optional): The event object that triggered the method. Defaults to None.

        Behavior:
        - If the entry field is empty, the method does nothing.
        - Sets the `categories_var` to the value entered in the entry field.
        - Adds the rating to the data structure that stores all user ratings and updates the navigation Treeview.
        - Moves to the next item to be rated.
        - Resets the entry field after the rating is saved.
        """
        if len(self.var_input.get()) == 0:
            return
        self.categories_var.set(self.var_input.get())
        self.label_text()
        self.next_cmd()
        self.var_input.delete(0, 'end')

    def cat_hotkey_cmd(self, event):
        """
        Handles the event when a category hotkey is pressed.

        Args:
            event (tkinter.Event): The event object containing information about the key press.

        This method is triggered when a user presses a number key (1-9) that corresponds to a category.
        It sets the category variable to the selected category, updates the rating data structure, and
        updates the navigation frame to reflect the new rating.
        """
        category_no = int(event.char) - 1
        self.categories_var.set(self.container.categories[category_no])
        self.label_text()

    def next_cmd(self, event=None):
        """
        Advance to the next text item in the list and update the display accordingly.

        This method is triggered by a right-arrow key press or a corresponding button click.
        It increments the current text index, updates the displayed text, and adjusts the 
        navigation tree view to reflect the new position. If a rating exists for the new 
        text item, it updates the rating display; otherwise, it resets the rating display.

        Parameters:
            event (tkinter.Event, optional): The event that triggered this method. Defaults to None.
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
        Navigate to the previous text item in the list and update the display accordingly.

        Args:
            event (tkinter.Event, optional): The event that triggered this command. Defaults to None.

        Behavior:
            - If the current text item is the first one, do nothing.
            - Otherwise, decrement the text index to point to the previous text item.
            - Update the displayed text and the selected category based on the new text index.
            - Adjust the navigation tree view to reflect the current text item.
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
            Save the current ratings to a file.

            This method is triggered when the user clicks the save button. It first checks if the text has been shuffled and, if so, undoes the shuffling to restore the original order. Then, it opens a file dialog to let the user choose a location and filename for saving the ratings. The ratings are saved in the selected file format (Excel, LibreOffice Calc, or CSV).

            Note:
                If the text has been shuffled, it will be unshuffled before saving.

            Raises:
                None

            Returns:
                None
    ""\""""
        if self.shuffler is not None:
            self.randomize('undo')
        self.focus_set()
        filename = tk.filedialog.asksaveasfilename(filetypes=[(
            'Excel files', '.xlsx .xls'), ('Libreoffice Calc files', '.ods'
            ), ('Csv files', '.csv')])
        self.container.filevalidation.write_file(filename, self.ratings)

    def delete_cmd(self):
        """
        Prompt the user to confirm if they want to discard the entire rating session. If confirmed, reset the ratings and update the frame accordingly.

        Focuses the widget to ensure key bindings are active.

        Displays a confirmation message box asking the user if they want to discard the entire rating session.

        If the user confirms, resets the categories variable and clears the ratings list.

        Resets the text index to 0 and updates the frame.

        If the user cancels, no action is taken.
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
        Updates the rating for the current text element based on the selected category.

        If the current text element is already rated with the selected category, it removes the rating.
        Otherwise, it updates or sets the rating for the current text element and updates the navigation tree view
        to reflect the rating status.

        Args:
            event (tkinter.Event, optional): The event that triggered this method. Defaults to None.
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
        Check if all text elements have been rated and prompt the user to save the ratings if completed.

        This method verifies whether the total number of ratings matches the number of text elements. 
        If all text elements have been rated, it displays a message box asking the user if they want to save the ratings.

        Returns:
            None
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
        Update the percentage label to reflect the current progress of ratings.

        Calculates the percentage of text elements that have been rated and updates the 
        percentage label accordingly. The label's style is also updated based on the 
        percentage to provide a visual indication of progress.

        Raises:
            ZeroDivisionError: If there are no text elements to rate.

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
        Prompt the user to save the current rating session and navigate back to the main frame.

        This method displays a message box asking the user if they want to save the current rating session.
        If the user chooses to save, it calls the `save_cmd` method to save the session.
        Afterwards, it reinitializes the frames and navigates back to the main frame.

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
        Display the help frame for the RateFrame.

        Args:
            event (tkinter.Event, optional): The event that triggered the help command. Defaults to None.
        """
        RateHelpFrame(self.container)

    def update_frame(self, mode=None):
        """
        Update the frame with the current text and ratings, and optionally randomize the text order.

        Parameters:
        mode (str, optional): If set to "do", the text and ratings will be randomized. Defaults to None.

        This method performs the following steps:
        1. Sets the focus to the frame for key bindings.
        2. Updates the text from the container's formatted text.
        3. Initializes the ratings list with empty tuples.
        4. Optionally randomizes the text and ratings if mode is "do".
        5. Deletes and repopulates the categories, questions, navigation, text, and percentage.
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
