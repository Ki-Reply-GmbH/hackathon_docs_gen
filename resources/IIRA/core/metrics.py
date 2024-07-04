import irrCAC as ir
from irrCAC.raw import CAC
import pingouin as pg
import pandas as pd
import numpy as np
import decimal as dec
import math
FIRST_REPLIACTE = 0
SECOND_REPLICATE = 1


class Metrics:
    """
    The Metrics class provides a comprehensive suite of methods for calculating various inter-rater reliability metrics.

    This class is designed to facilitate the analysis of ratings data by offering methods to compute several reliability coefficients, including Cohen's Kappa, Fleiss' Kappa, Gwet's AC, Krippendorff's Alpha, the G-index, and the Intraclass Correlation Coefficient (ICC). Additionally, it can calculate the overall agreement among raters.

    Attributes:
        debug (bool): Flag to enable or disable debug mode.
        scale_format (str): The format of the scale, either "ordinal" or "nominal".
        categories (list): The list of categories used in the ratings.
        ratings (pd.DataFrame): The DataFrame containing the ratings.
        quantity_subjects (int): The number of subjects in the ratings.
        replications (int): The number of replications, default is 2.
        weights (list): The list of weights for the categories.
        analysis (object): The analysis object created based on the scale format.

    Methods:
        cohens_kappa(): Calculate Cohen's Kappa coefficient for inter-rater reliability.
        fleiss_kappa(): Calculate Fleiss' Kappa, a measure of inter-rater reliability.
        gwets_ac(): Calculate Gwet's AC coefficient for inter-rater reliability.
        krippendorfs_alpha(): Calculate Krippendorff's Alpha, a measure of inter-rater reliability.
        g_index(): Calculate the G-index, a measure of inter-rater reliability.
        icc(): Calculate the Intraclass Correlation Coefficient (ICC) for the given ratings.
        overall_agreement(): Calculate the overall agreement among raters.
    """

    def __init__(self, scale_format, categories, ratings, weights):
        """
                ""\"
                Initialize the Metrics object with the given parameters and perform the appropriate analysis.

                Parameters:
                scale_format (str): The format of the scale, either "ordinal" or "nominal".
                categories (list): The list of categories used in the ratings.
                ratings (pd.DataFrame): The DataFrame containing the ratings.
                weights (list): The list of weights for the categories.

                Attributes:
                debug (bool): Flag to enable or disable debug mode.
                scale_format (str): The format of the scale.
                categories (list): The list of categories used in the ratings.
                ratings (pd.DataFrame): The DataFrame containing the ratings.
                quantity_subjects (int): The number of subjects in the ratings.
                replications (int): The number of replications, default is 2.
                weights (list): The list of weights for the categories.
                analysis (object): The analysis object created based on the scale format.
                ""\"
        """
        self.debug = False
        self.scale_format = scale_format
        self.categories = categories
        self.ratings = ratings
        self.quantity_subjects = len(self.ratings)
        self.replications = 2
        self.weights = weights
        self.analysis = None
        if scale_format == 'ordinal' or scale_format == 'nominal':
            try:
                self.analysis = CAC(ratings=self.ratings, weights=self.
                    weights, categories=self.categories, digits=4)
            except Exception as e:
                print('Exception creating irrCAC analysis: ' + str(e))
        else:
            try:
                self.analysis = self.icc()
            except Exception as e:
                print('Exception creating pingouin analysis: ' + str(e))
        dec.setcontext(dec.Context(prec=34))
        if self.debug:
            print('Ratings')
            print('len(ratings): ' + str(len(self.ratings)))
            print('len(ratings.columns): ' + str(len(self.ratings.columns)))
            print(self.ratings)
            print()
            print('Analyse')
            print(self.analysis)
            print()
            if (self.scale_format == 'ordinal' or self.scale_format ==
                'nominal'):
                print("Cohen's Kappa")
                print(self.analysis.conger())
                print()
                print('Fleiss Kappa')
                print(self.analysis.fleiss())
                print()
                print("Gwet's AC")
                print(self.analysis.gwet())
                print()
                print("Krippendorff's Alpha")
                print(self.analysis.krippendorff())
                print()

    def cohens_kappa(self):
        """
            ""\"
            Calculate Cohen's Kappa coefficient for inter-rater reliability.

            Cohen's Kappa is a statistic that measures inter-rater agreement for 
            qualitative (categorical) items. It is generally thought to be a more 
            robust measure than simple percent agreement calculation since Cohen's 
            Kappa takes into account the agreement occurring by chance.

            Returns:
                float: The coefficient value of Cohen's Kappa.
    ""\""""
        return self.analysis.conger()['est']['coefficient_value']

    def fleiss_kappa(self):
        """
        """
        return self.analysis.fleiss()['est']['coefficient_value']

    def gwets_ac(self):
        """
        """
        return self.analysis.gwet()['est']['coefficient_value']

    def krippendorfs_alpha(self):
        """
                ""\"
                Calculate Krippendorff's Alpha, a measure of inter-rater reliability.

                Returns:
                    float: The coefficient value of Krippendorff's Alpha.
        ""\""""
        return self.analysis.krippendorff()['est']['coefficient_value']

    def g_index(self):
        """
        Calculate the G-index, a measure of inter-rater reliability.

        The G-index is calculated based on the overall agreement among raters and the number of categories.

        Returns:
            float: The G-index value rounded to four decimal places.
        """
        q = len(self.categories)
        p_a = self.overall_agreement()
        g_index = (p_a - dec.Decimal('1') / q) / (dec.Decimal('1') - dec.
            Decimal('1') / q)
        return float(round(g_index, 4))

    def icc(self):
        """
                ""\"
                Calculate the Intraclass Correlation Coefficient (ICC) for the given ratings.

                This method transforms the ratings data into a format suitable for the 
                `pingouin` library's `intraclass_corr` function, which computes the ICC.
                The ICC is a measure of the reliability of ratings and is used to assess 
                the consistency or reproducibility of quantitative measurements made by 
                different raters measuring the same quantity.

                Returns:
                    DataFrame: A DataFrame containing the ICC results, including the 
                    coefficient values and other statistics.

                Raises:
                    Exception: If there is an error during the calculation of the ICC.
        ""\""""
        pg_targets = []
        pg_raters = []
        pg_ratings = []
        for i in range(len(self.ratings.columns)):
            for j in range(len(self.ratings)):
                pg_targets.append(j)
                pg_raters.append(self.ratings.columns[i])
            pg_ratings += list(self.ratings[self.ratings.columns[i]])
        df = pd.DataFrame({'pg_targets': pg_targets, 'pg_raters': pg_raters,
            'pg_ratings': pg_ratings})
        if self.debug:
            print('pg_targets')
            print(pg_targets)
            print()
            print('pg_raters')
            print(pg_raters)
            print()
            print('pg_ratings')
            print(pg_ratings)
            print()
        icc = pg.intraclass_corr(data=df, targets='pg_targets', raters=
            'pg_raters', ratings='pg_ratings', nan_policy='omit').round(4)
        return icc

    def overall_agreement(self):
        """
        Calculate the overall agreement among raters.

        This method computes the proportion of subjects for which the ratings are in agreement 
        across multiple replications. The calculation method varies depending on the number of 
        replications:
        - For two replications, it calculates the proportion of subjects where both replications 
          have the same rating.
        - For more than two replications, it uses a formula to account for the agreement across 
          multiple replications.

        Returns:
            decimal.Decimal: The overall agreement proportion.

        Raises:
            ValueError: If there are not enough replications per subject to calculate an overall agreement.
        """
        q = len(self.categories)
        p_a = dec.Decimal('0')
        if self.replications == 2:
            for k in range(q):
                current_cat = self.categories[k]
                subject_kk = dec.Decimal('0')
                for subject in self.ratings:
                    if self.ratings[subject][FIRST_REPLIACTE
                        ] == current_cat and self.ratings[subject][
                        FIRST_REPLIACTE] == self.ratings[subject][
                        SECOND_REPLICATE]:
                        subject_kk += dec.Decimal('1')
                p_kk = subject_kk
                p_a += p_kk / self.quantity_subjects
            return p_a
        elif self.replications > 2:
            m = self.quantity_subjects
            n = self.replications
            for i in self.ratings:
                for k in range(q):
                    n_i_k = dec.Decimal('0')
                    for replicate_label in self.ratings[i]:
                        if replicate_label == self.categories[k]:
                            n_i_k += dec.Decimal('1')
                    p_a += n_i_k * (n_i_k - 1) / (n * (n - 1))
            return p_a / m
        else:
            raise ValueError(
                'Not enough replications per subject to calculate an overall agreement.'
                )


def map_metrics(metric):
    """
    Map a given metric name to its corresponding method name in the Metrics class.

    This function takes a metric name as input and returns the corresponding method name 
    that can be used to calculate that metric in the Metrics class.

    Parameters:
        metric (str): The name of the metric to be mapped. Expected values are:
                      - "Cohen's-|Conger's κ"
                      - "Fleiss' κ"
                      - "Krippendorff's α"
                      - "Gwet's AC"

    Returns:
        str: The corresponding method name for the given metric.

    Examples:
        >>> map_metrics("Cohen's-|Conger's κ")
        'conger'
        >>> map_metrics("Fleiss' κ")
        'fleiss'
        >>> map_metrics("Krippendorff's α")
        'krippendorff'
        >>> map_metrics("Gwet's AC")
        'gwet'
    """
    if metric == "Cohen's-|Conger's κ":
        return 'conger'
    elif metric == "Fleiss' κ":
        return 'fleiss'
    elif metric == "Krippendorff's α":
        return 'krippendorff'
    elif metric == "Gwet's AC":
        return 'gwet'
