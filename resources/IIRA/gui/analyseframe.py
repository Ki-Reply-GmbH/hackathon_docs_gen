import tkinter as tk
from tkinter import ttk, messagebox
from math import isnan
from gui.containerframe import ContainerFrame
from gui.helperframes import ScrollFrame, PrepAnalyseHelpFrame, ResultsHelpFrame
from core.create_analyses import CreateAnalyses
from core.fileinteraction import write_excel
from core.metrics import map_metrics
selected_intra_ids = []
selected_inter_ids = []
selected_intra_metrics = []
selected_inter_metrics = []


class AnalyseFrame(ContainerFrame):
    """
    The AnalyseFrame class is designed to facilitate the preparation and execution of reliability analysis in a Tkinter-based GUI application. It provides functionalities for selecting raters and metrics for both intra-rater and inter-rater reliability studies.

    Attributes:
        metrics (list): A list to store selected metrics.
        intra_kappa (tk.IntVar): Variable for Cohen's-|Conger's Kappa metric.
        intra_fleiss_kappa (tk.IntVar): Variable for Fleiss' Kappa metric.
        intra_alpha_coefficient (tk.IntVar): Variable for Krippendorff's Alpha metric.
        intra_ac (tk.IntVar): Variable for Gwet's AC metric.
        intra_icc (tk.IntVar): Variable for ICC metric.
        intra_metrics (dict): Dictionary mapping intra-rater metrics to their respective variables.
        inter_kappa (tk.IntVar): Variable for Cohen's-|Conger's Kappa metric.
        inter_fleiss_kappa (tk.IntVar): Variable for Fleiss' Kappa metric.
        inter_alpha_coefficient (tk.IntVar): Variable for Krippendorff's Alpha metric.
        inter_ac (tk.IntVar): Variable for Gwet's AC metric.
        inter_icc (tk.IntVar): Variable for ICC metric.
        inter_metrics (dict): Dictionary mapping inter-rater metrics to their respective variables.
        intra_ids (dict): Dictionary to store intra-rater IDs.
        inter_ids (dict): Dictionary to store inter-rater IDs.
        rater_container (ScrollFrame): Scrollable frame for rater selection.
        toggle_ids (ttk.Button): Button to toggle selection of all rater IDs.
        metrics_container (ttk.Frame): Frame for metrics selection.
        toggle_metrics (ttk.Button): Button to toggle selection of all metrics.

    Superclass:
        tk.Frame: The AnalyseFrame class is derived from the Tkinter Frame class.
    """

    def __init__(self, container):
        """
        ""\"
        Initialize the AnalyseFrame with the given container.

        Args:
            container (tk.Tk or tk.Frame): The parent container for this frame.

        Attributes:
            metrics (list): A list to store selected metrics.
            intra_kappa (tk.IntVar): Variable for Cohen's-|Conger's Kappa metric.
            intra_fleiss_kappa (tk.IntVar): Variable for Fleiss' Kappa metric.
            intra_alpha_coefficient (tk.IntVar): Variable for Krippendorff's Alpha metric.
            intra_ac (tk.IntVar): Variable for Gwet's AC metric.
            intra_icc (tk.IntVar): Variable for ICC metric.
            intra_metrics (dict): Dictionary mapping intra-rater metrics to their respective variables.
            inter_kappa (tk.IntVar): Variable for Cohen's-|Conger's Kappa metric.
            inter_fleiss_kappa (tk.IntVar): Variable for Fleiss' Kappa metric.
            inter_alpha_coefficient (tk.IntVar): Variable for Krippendorff's Alpha metric.
            inter_ac (tk.IntVar): Variable for Gwet's AC metric.
            inter_icc (tk.IntVar): Variable for ICC metric.
            inter_metrics (dict): Dictionary mapping inter-rater metrics to their respective variables.
            intra_ids (dict): Dictionary to store intra-rater IDs.
            inter_ids (dict): Dictionary to store inter-rater IDs.
            rater_container (ScrollFrame): Scrollable frame for rater selection.
            toggle_ids (ttk.Button): Button to toggle selection of all rater IDs.
            metrics_container (ttk.Frame): Frame for metrics selection.
            toggle_metrics (ttk.Button): Button to toggle selection of all metrics.
        ""\"
        """
        self.metrics = []
        self.intra_kappa = tk.IntVar()
        self.intra_fleiss_kappa = tk.IntVar()
        self.intra_alpha_coefficient = tk.IntVar()
        self.intra_ac = tk.IntVar()
        self.intra_icc = tk.IntVar()
        self.intra_metrics = {"Cohen's-|Conger's κ": self.intra_kappa,
            "Fleiss' κ": self.intra_fleiss_kappa, "Krippendorff's α": self.
            intra_alpha_coefficient, "Gwet's AC": self.intra_ac, 'ICC':
            self.intra_icc}
        self.inter_kappa = tk.IntVar()
        self.inter_fleiss_kappa = tk.IntVar()
        self.inter_alpha_coefficient = tk.IntVar()
        self.inter_ac = tk.IntVar()
        self.inter_icc = tk.IntVar()
        self.inter_metrics = {"Cohen's-|Conger's κ": self.inter_kappa,
            "Fleiss' κ": self.inter_fleiss_kappa, "Krippendorff's α": self.
            inter_alpha_coefficient, "Gwet's AC": self.inter_ac, 'ICC':
            self.inter_icc}
        self.intra_ids = {}
        self.inter_ids = {}
        super().__init__(container)
        container.style.configure('AnalyseFrame.TButton', font='Arial 15',
            foreground='black', width=15)
        left_frame = ttk.Frame(self, style='Card', padding=(5, 6, 7, 8))
        right_frame = ttk.Frame(self, style='Card', padding=(5, 6, 7, 8))
        rater_label = ttk.Label(left_frame, font='Arial 20', text=
            '1. Auswahl der Bewerter')
        self.rater_container = ScrollFrame(left_frame)
        self.toggle_ids = ttk.Button(left_frame, text='Alle auswählen',
            style='AnalyseFrame.TButton', command=lambda : self.toggle('id'))
        metrics_label = ttk.Label(right_frame, font='Arial 20', text=
            '2. Auswahl der Metriken')
        self.metrics_container = ttk.Frame(right_frame)
        self.toggle_metrics = ttk.Button(right_frame, text='Alle auswählen',
            style='AnalyseFrame.TButton', command=lambda : self.toggle(
            'metric'))
        start_btn = ttk.Button(self, text='Analyse Starten', style=
            'AnalyseFrame.TButton', command=lambda : self.analyse_start(
            container))
        self.menu_bar.grid(row=0, column=0, sticky='nsew')
        left_frame.grid(row=1, column=0, sticky='nsew', padx=50, pady=50)
        right_frame.grid(row=1, column=1, sticky='nsew', padx=50, pady=50)
        rater_label.pack(side='top', padx=25, pady=10)
        self.rater_container.pack(side='top', fill='y', expand=True, padx=
            25, pady=50)
        self.toggle_ids.pack(side='bottom')
        metrics_label.pack(side='top', padx=25, pady=10)
        self.metrics_container.pack(side='top', padx=25, pady=50)
        self.toggle_metrics.pack(side='bottom')
        start_btn.grid(row=2, column=0, columnspan=2, pady=25)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def analyse_start(self, container):
        """
        Start the analysis process by collecting selected metrics and IDs for intra-rater and inter-rater reliability studies. 
        Validates the selections and displays error messages if the selections are invalid. 
        If the selections are valid, it updates the results frame and navigates to it.

        Args:
            container (tk.Tk): The main container of the application.
        """
        global selected_intra_metrics
        for metric in self.intra_metrics:
            if self.intra_metrics[metric].get(
                ) == 1 and metric not in selected_intra_metrics:
                selected_intra_metrics.append(metric)
        global selected_inter_metrics
        for metric in self.inter_metrics:
            if self.inter_metrics[metric].get(
                ) == 1 and metric not in selected_inter_metrics:
                selected_inter_metrics.append(metric)
        global selected_intra_ids
        for id in self.intra_ids:
            if self.intra_ids[id].get() == 1 and id not in selected_intra_ids:
                selected_intra_ids.append(id)
        global selected_inter_ids
        for id in self.inter_ids:
            if self.inter_ids[id].get() == 1 and id not in selected_inter_ids:
                selected_inter_ids.append(id)
        if len(selected_inter_ids) == 1:
            messagebox.showerror('Ungültige Eingabe',
                'Es kann keine Interrater-Untersuchung von nur einer Bewerter-ID berechnet werden.'
                )
            selected_intra_metrics = []
            selected_inter_metrics = []
            selected_intra_ids = []
            selected_inter_ids = []
            return
        elif len(selected_inter_ids) == 0 and len(selected_inter_ids) == 0:
            messagebox.showerror('Ungültige Eingabe',
                "Bitte Bewerter-ID's für die Reliabilitätsuntersuchung auswählen."
                )
            selected_intra_metrics = []
            selected_inter_metrics = []
            return
        elif len(selected_intra_metrics) == 0 and len(selected_inter_metrics
            ) == 0:
            messagebox.showerror('Ungültige Eingabe',
                'Bitte Metriken für die Reliabilitätsuntersuchung auswählen.')
            selected_intra_ids = []
            selected_inter_ids = []
            return
        container.frames['ResultsFrame'].update_frame()
        container.show_frame('ResultsFrame')

    def populate_rater_container(self):
        """
        Populate the rater container with rater IDs and their corresponding Intrarater and Interrater selection variables.

        This method initializes the `intra_ids` and `inter_ids` dictionaries with `IntVar` objects for each rater ID, 
        allowing the user to select or deselect raters for Intrarater and Interrater reliability analysis. It then 
        creates a table in the `rater_container` to display these options.

        The table will have three columns: "ID", "Intrarater", and "Interrater".

        Returns:
            None
        """
        headings = ['ID', 'Intrarater', 'Interrater']
        content = []
        for id in self.container.rater_ids:
            self.intra_ids[id] = tk.IntVar()
            self.inter_ids[id] = tk.IntVar()
            content.append([str(id), self.intra_ids[id], self.inter_ids[id]])
        self.create_table(self.rater_container.viewPort, headings, content)

    def populate_metrics_container(self):
        """
        Populate the metrics container with appropriate metrics based on the scale format.

        This method populates the metrics container with a list of metrics that are relevant 
        to the scale format specified in the container. It creates a table with the metrics 
        and their corresponding intrarater and interrater variables.

        The metrics are determined based on the following scale formats:
        - "nominal": Cohen's-|Conger's κ, Fleiss' κ, Krippendorff's α, Gwet's AC
        - "ordinal": Cohen's-|Conger's κ, Fleiss' κ, Krippendorff's α, Gwet's AC
        - "intervall": ICC
        - "rational": ICC

        The table created has the following columns:
        - Metrik: The name of the metric
        - Intrarater: The variable associated with the intrarater metric
        - Interrater: The variable associated with the interrater metric
        """
        if self.container.scale_format == 'nominal':
            self.metrics = ["Cohen's-|Conger's κ", "Fleiss' κ",
                "Krippendorff's α", "Gwet's AC"]
        elif self.container.scale_format == 'ordinal':
            self.metrics = ["Cohen's-|Conger's κ", "Fleiss' κ",
                "Krippendorff's α", "Gwet's AC"]
        elif self.container.scale_format == 'intervall':
            self.metrics = ['ICC']
        elif self.container.scale_format == 'rational':
            self.metrics = ['ICC']
        headings = ['Metrik', 'Intrarater', 'Interrater']
        content = []
        for metric in self.metrics:
            content.append([metric, self.map_metric_to_var('intra', metric),
                self.map_metric_to_var('inter', metric)])
        self.create_table(self.metrics_container, headings, content)

    def map_metric_to_var(self, mode, metric_name):
        """
        Map a metric name to its corresponding Tkinter variable.

        Args:
            mode (str): The mode of the metric, either 'intra' or 'inter'.
            metric_name (str): The name of the metric to map.

        Returns:
            tk.IntVar: The Tkinter variable associated with the given metric name and mode.
        """
        if mode == 'intra':
            if metric_name == "Cohen's-|Conger's κ":
                return self.intra_kappa
            elif metric_name == "Fleiss' κ":
                return self.intra_fleiss_kappa
            elif metric_name == "Krippendorff's α":
                return self.intra_alpha_coefficient
            elif metric_name == "Gwet's AC":
                return self.intra_ac
            elif metric_name == 'ICC':
                return self.intra_icc
        elif mode == 'inter':
            if metric_name == "Cohen's-|Conger's κ":
                return self.inter_kappa
            elif metric_name == "Fleiss' κ":
                return self.inter_fleiss_kappa
            elif metric_name == "Krippendorff's α":
                return self.inter_alpha_coefficient
            elif metric_name == "Gwet's AC":
                return self.inter_ac
            elif metric_name == 'ICC':
                return self.inter_icc

    def toggle(self, mode):
        """
        Toggle the selection state of all items in a given mode (either 'id' or 'metric').

        Args:
            mode (str): The mode to toggle, either 'id' for rater IDs or 'metric' for metrics.

        The function checks the current selection state of all items in the specified mode.
        If all items are selected, it deselects all of them and updates the button text to "Alle auswählen".
        If not all items are selected, it selects all of them and updates the button text to "Alle abwählen".
        """
        if mode == 'id':
            intra_dic = self.intra_ids
            inter_dic = self.inter_ids
            btn = self.toggle_ids
        if mode == 'metric':
            intra_dic = self.intra_metrics
            inter_dic = self.inter_metrics
            btn = self.toggle_metrics
        all_set = True
        for i in intra_dic:
            if mode == 'metric':
                if i not in self.metrics:
                    continue
            if intra_dic[i].get() == 0:
                all_set = False
                break
        for i in inter_dic:
            if mode == 'metric':
                if i not in self.metrics:
                    continue
            if inter_dic[i].get() == 0:
                all_set = False
                break
        if all_set:
            for i in intra_dic:
                intra_dic[i].set(0)
            for i in inter_dic:
                inter_dic[i].set(0)
            btn.config(text='Alle auswählen')
        else:
            for i in intra_dic:
                if mode == 'metric':
                    if i not in self.metrics:
                        continue
                intra_dic[i].set(1)
            for i in inter_dic:
                if mode == 'metric':
                    if i not in self.metrics:
                        continue
                inter_dic[i].set(1)
            btn.config(text='Alle abwählen')

    def help_cmd(self, event=None):
        """
                ""\"
                Opens the help frame for the analysis preparation.

                This method creates an instance of the `PrepAnalyseHelpFrame` class,
                which displays the help information related to the analysis preparation
                process.

                Args:
                    event (tkinter.Event, optional): The event that triggered this method. Defaults to None.
                ""\"
        """
        PrepAnalyseHelpFrame(self.container)

    def update_frame(self):
        """
        ""\"
        Update the frame by populating the rater and metrics containers.

        This method is responsible for updating the user interface by populating the 
        rater container and the metrics container with the relevant data. It calls 
        two helper methods: `populate_rater_container` and `populate_metrics_container`.

        The `populate_rater_container` method fills the rater container with the 
        available rater IDs and their corresponding intra- and inter-rater options.

        The `populate_metrics_container` method fills the metrics container with the 
        available metrics based on the scale format of the data.

        This method is typically called when the frame needs to be refreshed or 
        re-initialized with updated data.
        ""\"
        """
        self.populate_rater_container()
        self.populate_metrics_container()


class ResultsFrame(ContainerFrame):
    """
    A frame for displaying and managing the results of reliability analyses.

    The ResultsFrame class is responsible for presenting the results of reliability analyses to the user. It provides functionalities to export these results to various file formats, access help specific to the results, and dynamically update the displayed data.

    Attributes:
        Inherits from a superclass (not specified in the provided context).

    Methods:
        - export_cmd: Exports the reliability analysis results to a file.
        - help_cmd: Opens the help frame specific to the ResultsFrame.
        - update_frame: Updates the frame with dynamically generated data.
    """

    def __init__(self, container):
        self.debug = True
        self.reliability_analyses = None
        super().__init__(container)
        container.style.configure('ResultsFrame.TButton', font='Arial 15',
            foreground='black')
        container.style.configure('TNotebook.Tab', font='Arial 15')
        center_container = ttk.Frame(self)
        self.notebook = ttk.Notebook(center_container)
        results_label = ttk.Label(center_container, font='Arial 20', text=
            'Ergebnisse')
        self.intrarater_frame = ttk.Frame(self.notebook)
        self.intrarater_results = ScrollFrame(self.intrarater_frame)
        self.intrarater_infos = ScrollFrame(self.intrarater_frame)
        self.interrater_frame = ttk.Frame(self.notebook)
        self.interrater_results = ttk.Frame(self.interrater_frame)
        self.interrater_infos = ScrollFrame(self.interrater_frame)
        export_btn = ttk.Button(center_container, text='Exportieren', style
            ='ResultsFrame.TButton', command=self.export_cmd)
        self.menu_bar.grid(row=0, column=0, sticky='nsew')
        center_container.grid(row=1, column=0, sticky='nsew', padx=15, pady=15)
        results_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)
        self.notebook.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        export_btn.grid(row=2, column=0)
        self.intrarater_results.pack(side='left', fill='both', expand=True,
            padx=(15, 0), pady=25)
        self.intrarater_infos.pack(side='right', fill='both', padx=(0, 15),
            pady=25)
        self.interrater_results.pack(side='left', fill='both', expand=True,
            padx=(15, 0), pady=25)
        self.interrater_infos.pack(side='right', fill='both', padx=(0, 15),
            pady=25)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        center_container.rowconfigure(1, weight=1)
        center_container.columnconfigure(0, weight=1)
        self.intrarater_frame.rowconfigure(0, weight=1)
        self.intrarater_frame.columnconfigure(0, weight=1)

    def calculate_results(self):
        """
        Calculate the reliability analysis results based on selected metrics and IDs.

        This method initializes the `CreateAnalyses` class with the selected intra-rater and inter-rater IDs and metrics, as well as other relevant parameters from the container. The results of the reliability analyses are stored in the `reliability_analyses` attribute.

        Attributes:
            selected_intra_ids (list): List of selected intra-rater IDs.
            selected_inter_ids (list): List of selected inter-rater IDs.
            selected_intra_metrics (list): List of selected intra-rater metrics.
            selected_inter_metrics (list): List of selected inter-rater metrics.
            container.scale_format (str): The scale format of the data (e.g., 'nominal', 'ordinal').
            container.categories (list): List of categories used in the analysis.
            container.weights (list): List of weights used in the analysis.
            container.filevalidation.labels (list): List of labels used in file validation.

        Returns:
            None
        """
        self.reliability_analyses = CreateAnalyses(selected_intra_ids,
            selected_inter_ids, selected_intra_metrics,
            selected_inter_metrics, self.container.scale_format, self.
            container.categories, self.container.weights, self.container.
            filevalidation.labels)

    def populate_intra_results(self):
        """
        ""\"
        Populate the intra-rater results in the results frame.

        This method populates the intra-rater results section of the results frame with the calculated reliability analysis results. It dynamically generates a table with the results for each selected intra-rater metric and rater ID. The table includes the metric values, the number of subjects, and the number of replicates for each rater ID.

        The method also handles cases where there are not enough ratings to calculate the metrics and displays appropriate information messages.

        If the scale format is nominal or ordinal, additional information such as the number of subjects and replicates is included in the table.

        Raises:
            Exception: If there is an error during the calculation of metric values.
        ""\"
        """
        if selected_intra_ids and selected_intra_metrics:
            self.notebook.add(self.intrarater_frame, text='Intra-Rater')
            headings = ['ID']
            for metric in selected_intra_metrics:
                headings.append(metric)
            if (self.container.scale_format == 'nominal' or self.container.
                scale_format == 'ordinal'):
                headings.append('#Subjects')
                headings.append('#Replicates')
            content = []
            not_enough_ratings = []
            if (self.container.scale_format == 'nominal' or self.container.
                scale_format == 'ordinal'):
                for rater_id in self.reliability_analyses.results['intra']:
                    quant_subjects = self.reliability_analyses.results['intra'
                        ][rater_id].n
                    quant_replicates = self.reliability_analyses.results[
                        'intra'][rater_id].r
                    if quant_replicates < 2 or quant_subjects < 1:
                        not_enough_ratings.append(str(rater_id))
                        continue
                    if self.debug:
                        print('populate_intra_results')
                        print('Rater id: ' + str(rater_id))
                        print('quant_subjects ' + str(quant_subjects))
                        print('quant_replicates ' + str(quant_replicates))
                        print()
                    row = []
                    cont = False
                    for metric in selected_intra_metrics:
                        metric_function_name = map_metrics(metric)
                        metric_value = -99
                        try:
                            metric_value = getattr(self.
                                reliability_analyses.results['intra'][
                                rater_id], metric_function_name)()['est'][
                                'coefficient_value']
                        except ZeroDivisionError:
                            metric_value = 1.0
                        except Exception as e:
                            print('Exception in populate_intra_results:' +
                                str(e))
                        if isnan(metric_value
                            ) and metric == "Cohen's-|Conger's κ":
                            metric_value = 1.0
                        row.append(str(metric_value))
                    if cont:
                        continue
                    row.insert(0, str(rater_id))
                    row.append(str(quant_subjects))
                    row.append(str(quant_replicates))
                    content.append(row)
            else:
                for rater_id in self.reliability_analyses.results['intra']:
                    row = [str(rater_id)]
                    metric_function_name = map_metrics(metric)
                    metric_value = -99
                    try:
                        metric_value = self.reliability_analyses.results[
                            'intra'][rater_id].iloc[2]['ICC']
                    except Exception as e:
                        print('Exception in populate_intra_results:' + str(e))
                    row.append(str(metric_value))
                    content.append(row)
            if self.debug:
                print('populate_intra_results')
                print('Headings')
                print(headings)
                print()
                print('Content')
                print(content)
                print()
            self.create_table(self.intrarater_results.viewPort, headings,
                content)
            intrarater_infolabel = ttk.Label(self.intrarater_infos.viewPort,
                font='Arial 20', text='Infos:')
            intrarater_info_list = ttk.Frame(self.intrarater_infos.viewPort)
            txt = 'Skalenformat: ' + self.container.scale_format
            scale_format_lbl = ttk.Label(intrarater_info_list, font=
                'Arial 18', text=txt)
            scale_format_lbl.pack(padx=5, pady=5, fill='x')
            if (self.container.scale_format == 'nominal' or self.container.
                scale_format == 'ordinal'):
                txt = 'Gewichte: ' + self.container.weights
                weights_lbl = ttk.Label(intrarater_info_list, font=
                    'Arial 18', text=txt)
                weights_lbl.pack(padx=5, pady=(5, 15), fill='x')
                if not_enough_ratings:
                    txt = 'Keine Subjects mehrfach\nbewertet:'
                    not_enough_ratings_lbl = ttk.Label(intrarater_info_list,
                        font='Arial 18', text=txt)
                    not_enough_ratings_lbl.pack(padx=5, pady=5, fill='x')
                    for rater_id in not_enough_ratings:
                        txt = '• ' + str(rater_id)
                        no_replicates = ttk.Label(intrarater_info_list,
                            font='Arial 18', text=txt)
                        no_replicates.pack(padx=5, pady=5, fill='x')
            intrarater_infolabel.pack(pady=15)
            intrarater_info_list.pack(fill='y')

    def populate_inter_results(self):
        """
        Populate the inter-rater results section of the results frame.

        This method populates the inter-rater results section of the results frame with the calculated reliability metrics. It dynamically generates the table headings and content based on the selected inter-rater metrics and the scale format of the data. The method also handles exceptions and ensures that the results are displayed correctly.

        The table created has the following columns:
        - For nominal or ordinal scale formats: the selected metrics, number of subjects, and number of raters.
        - For interval or rational scale formats: the selected metrics.

        If there are any issues during the calculation of the metrics, the method catches the exceptions and prints them for debugging purposes.

        Returns:
            None
        """
        if selected_inter_ids and selected_inter_metrics:
            self.notebook.add(self.interrater_frame, text='Inter-Rater')
            headings = []
            for metric in selected_inter_metrics:
                headings.append(metric)
            if (self.container.scale_format == 'nominal' or self.container.
                scale_format == 'ordinal'):
                headings.append('#Subjects')
                headings.append('#Rater')
            content = []
            row = []
            if (self.container.scale_format == 'nominal' or self.container.
                scale_format == 'ordinal'):
                for metric in selected_inter_metrics:
                    metric_function_name = map_metrics(metric)
                    metric_value = -99
                    try:
                        metric_value = getattr(self.reliability_analyses.
                            results['inter'], metric_function_name)()['est'][
                            'coefficient_value']
                    except Exception as e:
                        print('Exception in populate_intra_results:' + str(e))
                    row.append(str(metric_value))
            else:
                metric_value = -99
                try:
                    metric_value = self.reliability_analyses.results['inter'
                        ].iloc[2]['ICC']
                except Exception as e:
                    print('Exception in populate_intra_results:' + str(e))
                row.append(str(metric_value))
                content.append(row)
            if (self.container.scale_format == 'nominal' or self.container.
                scale_format == 'ordinal'):
                quant_subjects = self.reliability_analyses.results['inter'].n
                row.append(str(quant_subjects))
                quant_raters = self.reliability_analyses.results['inter'].r
                row.append(str(quant_raters))
                content.append(row)
            self.create_table(self.interrater_results, headings, content)
            interrater_infolabel = ttk.Label(self.interrater_infos, font=
                'Arial 18', text='Infos:')
            interrater_info_list = ttk.Frame(self.interrater_infos)
            txt = 'Skalenformat: ' + self.container.scale_format
            scale_format_lbl = ttk.Label(interrater_info_list, font=
                'Arial 18', text=txt)
            scale_format_lbl.pack(padx=5, pady=5, fill='x')
            if (self.container.scale_format == 'nominal' or self.container.
                scale_format == 'ordinal'):
                txt = 'Gewichte: ' + self.container.weights
                weights_lbl = ttk.Label(interrater_info_list, font=
                    'Arial 18', text=txt)
                weights_lbl.pack(padx=5, pady=(5, 15), fill='x')
            interrater_infolabel.pack(pady=15)
            interrater_info_list.pack(pady=15)

    def export_cmd(self):
        """
        Export the reliability analysis results to a file.

        This method opens a file dialog to ask the user for a filename and file type 
        to save the results of the reliability analyses. The results are then written 
        to the specified file in the chosen format (Excel, LibreOffice Calc, or CSV).

        Raises:
            Exception: If there is an error during the file writing process.
        """
        filename = tk.filedialog.asksaveasfilename(filetypes=[(
            'Excel files', '.xlsx .xls'), ('Libreoffice Calc files', '.ods'
            ), ('Csv files', '.csv')])
        write_excel(self.reliability_analyses, selected_intra_ids,
            selected_intra_metrics, selected_inter_ids,
            selected_inter_metrics, self.container.scale_format, filename)

    def help_cmd(self, event=None):
        """
        Die Funktion öffnet das Helpframe.
        """
        ResultsHelpFrame(self.container)

    def update_frame(self):
        """
        Die Funktion füllt den Frame mit dynamisch erzeugten Daten.
        """
        self.calculate_results()
        self.populate_intra_results()
        self.populate_inter_results()
