from math import nan, isnan
from core.metrics import Metrics
from pprint import pprint
import pandas as pd
import numpy as np
TEXT = 0
LABEL = 1
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class CreateAnalyses:
    """
    The CreateAnalyses class is designed to perform both intra-rater and inter-rater analyses on a given dataset. 

    This class provides methods to:
    - Initialize the analysis parameters.
    - Perform intra-rater analysis by iterating over a list of IDs and applying specified metrics.
    - Perform inter-rater analysis by aggregating ratings from multiple raters and conducting statistical analysis.
    - Retrieve intra-rater ratings for a specific ID.
    - Collect and organize inter-rater ratings into a structured format.

    Attributes:
        intra_id_list (list): List of IDs for intra-rater analysis.
        inter_id_list (list): List of IDs for inter-rater analysis.
        intra_metrics (list): List of metrics for intra-rater analysis.
        inter_metrics (list): List of metrics for inter-rater analysis.
        scale_format (str): The format of the scale used in the analysis.
        categories (list): List of categories used in the analysis.
        weights (list): List of weights applied to the metrics.
        data (dict): Data required for the analysis, formatted similarly to the labels format in the FileValidation class.
        results (dict): Dictionary to store the results of the analyses.

    Superclass:
        The class does not explicitly inherit from any superclass or implement any interface.
    """

    def __init__(self, intra_id_list, inter_id_list, intra_metrics,
        inter_metrics, scale_format, categories, weights, data):
        """
        ""\"
        Initialize the CreateAnalyses class with the given parameters and perform initial analyses.

        Args:
            intra_id_list (list): List of IDs for intra-rater analysis.
            inter_id_list (list): List of IDs for inter-rater analysis.
            intra_metrics (list): List of metrics for intra-rater analysis.
            inter_metrics (list): List of metrics for inter-rater analysis.
            scale_format (str): The format of the scale used in the analysis.
            categories (list): List of categories used in the analysis.
            weights (list): List of weights applied to the metrics.
            data (dict): Data required for the analysis, formatted similarly to the labels format in the FileValidation class.

        Attributes:
            debug (bool): Flag to enable or disable debug mode.
            intra_id_list (list): List of IDs for intra-rater analysis.
            inter_id_list (list): List of IDs for inter-rater analysis.
            intra_metrics (list): List of metrics for intra-rater analysis.
            inter_metrics (list): List of metrics for inter-rater analysis.
            scale_format (str): The format of the scale used in the analysis.
            categories (list): List of categories used in the analysis.
            weights (list): List of weights applied to the metrics.
            data (dict): Data required for the analysis, formatted similarly to the labels format in the FileValidation class.
            results (dict): Dictionary to store the results of the analyses.

        Actions:
            - Initializes the analysis parameters.
            - Performs intra-rater analysis if intra_id_list and intra_metrics are provided.
            - Performs inter-rater analysis if inter_id_list and inter_metrics are provided.
            - Prints debug information if debug mode is enabled.
        ""\"
        """
        self.debug = True
        self.intra_id_list = intra_id_list
        self.inter_id_list = inter_id_list
        self.intra_metrics = intra_metrics
        self.inter_metrics = inter_metrics
        self.scale_format = scale_format
        self.categories = categories
        self.weights = weights
        self.data = data
        self.results = {'intra': {}, 'inter': {}}
        if self.intra_id_list and self.intra_metrics:
            if self.debug:
                print('Enter intra analysis')
            self.create_intra_analyses()
        if self.inter_id_list and self.inter_metrics:
            if self.debug:
                print('Enter inter analysis')
            self.create_inter_analyses()
        if self.debug:
            print("Intra ID's:")
            print(self.intra_id_list)
            print('Intra Metrics:')
            print(self.intra_metrics)
            print()
            print("Inter ID's:")
            print(self.inter_id_list)
            print('Inter Metrics:')
            print(self.inter_metrics)
            print()
            print('Skalenformat')
            print(self.scale_format)
            print()
            print('Kategorien')
            print(self.categories)
            print()
            print('Gewichte')
            print(self.weights)
            print()
            print('Daten')
            print(self.data)
            print()
            print('Results')
            print(self.results)
            print()

    def create_intra_analyses(self):
        """
            ""\"
            Perform intra-rater analysis for each ID in the intra_id_list.

            This method iterates over the list of IDs specified for intra-rater analysis,
            retrieves the corresponding ratings, and applies the defined metrics to compute
            the analysis results. The results are stored in the 'results' attribute under
            the 'intra' key.

            The method also prints debug information if the debug mode is enabled.

            Returns:
                None
    ""\""""
        for id in self.intra_id_list:
            self.results['intra'][id] = {}
            ratings = self.find_intra_ratings(id)
            if self.debug:
                print('Intra Ratings for ID ' + str(id) + ':')
                print(ratings)
                print()
            calculations = Metrics(self.scale_format, self.categories,
                ratings, self.weights)
            self.results['intra'][id] = calculations.analysis
            if self.debug:
                print('Intra Analyse for ID ' + str(id) + ':')
                print(self.results['intra'][id])
                print()

    def create_inter_analyses(self):
        """
        Perform inter-rater analysis by aggregating ratings from multiple raters and conducting statistical analysis.

        This method collects ratings from multiple raters for the IDs specified in `inter_id_list`, 
        aggregates them, and then applies the specified metrics to perform the analysis. 
        The results are stored in the `results` dictionary under the 'inter' key.

        Attributes:
            None

        Returns:
            None
        """
        ratings = self.find_inter_ratings()
        if self.debug:
            print('Inter Ratings:')
            print(ratings)
            print()
        calculations = Metrics(self.scale_format, self.categories, ratings,
            self.weights)
        self.results['inter'] = calculations.analysis

    def find_intra_ratings(self, id):
        """
        Retrieve and organize intra-rater ratings for a specific ID.

        This method processes the ratings data for a given ID, filtering out invalid or empty ratings,
        and organizes the valid ratings into a structured format suitable for further analysis.

        Args:
            id (str): The identifier for which intra-rater ratings are to be retrieved.

        Returns:
            pd.DataFrame: A DataFrame where the index represents the text being rated and the columns
            contain the corresponding ratings. Only texts with at least two ratings are included.
        """
        ret = {}
        for rating in self.data[id]:
            if not isinstance(rating[LABEL], str) or rating[LABEL] == '':
                continue
            if rating[TEXT] in ret:
                ret[rating[TEXT]].append(rating[LABEL])
            else:
                ret[rating[TEXT]] = [rating[LABEL]]
        if self.debug:
            ret_rmv = {k: v for k, v in ret.items() if len(v) >= 2}
        return pd.DataFrame.from_dict(ret_rmv, orient='index')

    def find_inter_ratings(self):
        """
        Collects and organizes inter-rater ratings into a structured format.

        This method iterates over the list of IDs specified for inter-rater analysis and aggregates the ratings from multiple raters. The ratings are organized into a dictionary where the keys are the text items being rated and the values are lists of ratings from different raters. The resulting dictionary is then converted into a pandas DataFrame for further analysis.

        Returns:
            pd.DataFrame: A DataFrame where the index represents the text items and the columns represent the ratings from different raters.
        """
        ret = {}
        for i, id in enumerate(self.inter_id_list):
            for rating in self.data[id]:
                if rating[TEXT] in ret:
                    if len(ret[rating[TEXT]]) > i:
                        continue
                    ret[rating[TEXT]].append(rating[LABEL])
                else:
                    ret[rating[TEXT]] = [rating[LABEL]]
        return pd.DataFrame.from_dict(ret, orient='index')
