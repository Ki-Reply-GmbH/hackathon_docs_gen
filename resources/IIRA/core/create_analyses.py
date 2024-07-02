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
    The CreateAnalyses class is designed to facilitate both intra-rater and inter-rater analyses using specified metrics, data, and configurations. It initializes with necessary parameters to set up the environment for these analyses and provides methods to conduct and retrieve results for intra and inter analyses separately. This class is essential for evaluating the consistency and reliability of ratings within and between different raters, making it suitable for statistical assessments in research studies or quality control processes.
    """

    def __init__(self, intra_id_list, inter_id_list, intra_metrics,
        inter_metrics, scale_format, categories, weights, data):
        """
        Initialize the CreateAnalyses class with necessary data for performing intra and inter analyses.

        Parameters:
            intra_id_list (list): List of IDs for intra analysis.
            inter_id_list (list): List of IDs for inter analysis.
            intra_metrics (object): Metrics object for intra analysis.
            inter_metrics (object): Metrics object for inter analysis.
            scale_format (str): The format of the scale used in the analysis.
            categories (list): List of categories involved in the analysis.
            weights (dict): Dictionary of weights for each category.
            data (dict): Data used for the analysis, formatted according to the labels format in the FileValidation class.
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
        Conducts intra-analysis for each ID in the intra_id_list using the provided data and metrics.

        This method iterates over each ID in the intra_id_list, retrieves the corresponding intra-ratings,
        and computes the analysis using the Metrics class. The results are stored in the 'results' dictionary
        under the 'intra' key, indexed by the ID. Debug information is printed if debugging is enabled.
        """
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
        Compiles inter-rater analysis results based on the provided inter-rater IDs and metrics.

        This method aggregates ratings from different raters for the same items, computes the analysis using the specified metrics, scale format, categories, and weights, and stores the results in the 'inter' key of the results dictionary.
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
        Extracts intra-rater ratings for a given ID from the dataset.

        This method processes the data for a specific ID to compile the ratings given by the same rater across multiple instances.
        It filters out entries where the label is missing or is a null value. It also ensures that only subjects rated more than once by the same rater are included in the final DataFrame, which is crucial for intra-rater reliability analysis.

        Parameters:
            id (int): The identifier for the rater whose intra-ratings are to be extracted.

        Returns:
            pd.DataFrame: A DataFrame where the index represents the subjects and the columns contain the ratings given by the rater.
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
        Compiles inter-rater ratings from multiple raters into a structured DataFrame.

        This method aggregates ratings from different raters specified in `self.inter_id_list` for each subject. It ensures that each subject's ratings are collected from all raters, avoiding duplicates that are only relevant for intra-rater analysis. The method constructs a dictionary where each key is a subject and the value is a list of ratings from different raters. This dictionary is then converted into a pandas DataFrame.

        Returns:
            pandas.DataFrame: A DataFrame where the index represents the subjects and each row contains the list of ratings provided by different raters.
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
