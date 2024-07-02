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
    The AnalyseFrame class is designed to facilitate the analysis of intra-rater and inter-rater reliability within a graphical user interface. It provides functionalities to initialize the analysis environment, populate it with necessary components like rater IDs and metrics, and manage the analysis process. This class handles user interactions, data validation, and result display, ensuring a comprehensive and user-friendly interface for reliability analysis tasks.
    """

    def __init__(self, container):
        """
            ""\"
            Initialize the AnalyseFrame with a specified container.

            This method sets up the frame for analysis, including the configuration of various
            metrics for intra-rater and inter-rater reliability analysis. It also initializes
            the GUI components such as buttons, labels, and frames necessary for the analysis
            process.

            Args:
            container (tk.Widget): The parent widget in which this frame is contained.
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
            ""\"
            Initiates the analysis process based on selected rater IDs and metrics.

            This method collects all selected intra-rater and inter-rater metrics and IDs,
            validates the selections, and proceeds to display the results in the ResultsFrame.
            It handles various validation checks such as ensuring there are enough raters for
            inter-rater analysis and that metrics and rater IDs are selected before proceeding.

            Parameters:
                container (tk.Frame): The parent container which holds the frame structure.

            Raises:
                tk.messagebox.showerror: If there is an invalid input such as only one rater ID
                                         for inter-rater analysis or no metrics/rater IDs selected.
            ""\"
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
            ""\"
            Populates the rater container with rater IDs and their corresponding checkbuttons for intra-rater and inter-rater selections.

            This method retrieves a list of rater IDs from the container's `rater_ids` attribute, initializes checkbutton variables
            for each rater ID for both intra-rater and inter-rater analysis, and creates a table in the rater container frame with
            these checkbuttons. Each row in the table corresponds to a rater ID and includes checkbuttons to select or deselect
            that ID for intra-rater and inter-rater analysis.
            ""\"
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
        Populates the metrics container based on the scale format of the data. It dynamically adjusts the available metrics
        for intrarater and interrater analysis based on the scale format (nominal, ordinal, interval, or rational).
        It then creates a table displaying these metrics with options to select for analysis.
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
            ""\"
            Maps a given metric name to its corresponding tkinter variable based on the mode.

            Args:
            mode (str): Specifies the mode as either 'intra' or 'inter'.
            metric_name (str): The name of the metric to map.

            Returns:
            tkinter.IntVar: The tkinter variable associated with the given metric name and mode.
            ""\"
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
            ""\"
            Toggles the selection state of all IDs or metrics based on the provided mode.

            This method checks if all IDs or metrics are selected. If they are, it deselects all;
            otherwise, it selects all. It also updates the button text accordingly to reflect the
            current state (either "Alle auswählen" for select all or "Alle abwählen" for deselect all).

            Parameters:
            - mode (str): Determines the type of items to toggle. Accepts 'id' for toggling rater IDs
                          or 'metric' for toggling metrics.
            ""\"
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
            Opens a help frame specific to the preparation and analysis phase.
            This frame provides guidance and information related to the analysis setup process.
            ""\"
        """
        PrepAnalyseHelpFrame(self.container)

    def update_frame(self):
        """
        Updates the frame by populating it with dynamically generated data. It calculates the results based on selected metrics and IDs, then populates the intra-rater and inter-rater results sections accordingly.
        """
        self.populate_rater_container()
        self.populate_metrics_container()


class ResultsFrame(ContainerFrame):
    """
    A class designed to manage and display reliability analysis results within a graphical user interface.

    This class, ResultsFrame, is responsible for initializing the analysis environment, calculating reliability metrics, and displaying these metrics for intra-rater and inter-rater reliability analyses. It supports various statistical methods and handles the export of results to different file formats. The class also provides a help section to guide users through the analysis process.

    Attributes:
        container (tk.Widget): The parent widget in which this frame is contained.
        reliability_analyses (dict): Stores the results of the reliability analyses.

    Methods:
        __init__(self, container): Initializes the frame with necessary GUI components.
        calculate_results(self): Performs the reliability calculations.
        populate_intra_results(self): Displays intra-rater reliability metrics.
        populate_inter_results(self): Displays inter-rater reliability metrics.
        export_cmd(self): Exports the analysis results to a file.
        help_cmd(self, event=None): Provides help related to the analysis setup.
        update_frame(self): Updates the frame with new data and recalculates results.
    """

    def __init__(self, container):
        """
            ""\"
            Initialize the AnalyseFrame with a specified container.

            This method sets up the frame for analysis, including the configuration of various
            metrics for intra-rater and inter-rater reliability analysis. It also initializes
            the GUI components such as buttons, labels, and frames necessary for the analysis
            process.

            Args:
            container (tk.Widget): The parent widget in which this frame is contained.
            ""\"
        """
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
            ""\"
            Calculate the reliability analyses based on the selected intra-rater and inter-rater IDs and metrics.
    
            This method initializes the reliability analyses using the selected IDs and metrics, along with
            additional parameters such as scale format, categories, weights, and labels from the container.
            The results are stored in the `reliability_analyses` attribute of the instance.
            ""\"
        """
        self.reliability_analyses = CreateAnalyses(selected_intra_ids,
            selected_inter_ids, selected_intra_metrics,
            selected_inter_metrics, self.container.scale_format, self.
            container.categories, self.container.weights, self.container.
            filevalidation.labels)

    def populate_intra_results(self):
        """
            ""\"
            Populates the intrarater results tab with calculated reliability metrics for selected intra-rater IDs.

            This method dynamically generates a table displaying the reliability metrics for each selected rater ID.
            It includes metrics such as Cohen's kappa, Fleiss' kappa, Krippendorff's alpha, Gwet's AC, and ICC,
            depending on the scale format (nominal, ordinal, interval, or ratio) and the selected metrics.
            Additional information such as the number of subjects and replicates (if applicable) is also displayed.

            The method handles cases where there are not enough ratings to compute the metrics, and it provides
            detailed debug information if the debug mode is enabled.
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
        Populates the inter-rater results tab with calculated metrics and displays them in a table format.

        This method checks if there are selected inter-rater IDs and metrics, and if so, it adds a new tab to the notebook widget for displaying inter-rater results. It constructs the table headers based on the selected metrics and, depending on the scale format, adds columns for the number of subjects and raters. The method calculates the metric values using the results from the reliability analyses and displays them in the table. Additionally, it provides information about the scale format and weights used in the analysis.
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

        This method prompts the user to specify a filename and file type, then exports the
        reliability analysis results to the chosen file format. Supported formats include
        Excel (.xlsx, .xls), LibreOffice Calc (.ods), and CSV (.csv). The method uses the
        `write_excel` function to handle the actual file writing process.
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
