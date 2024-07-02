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
    The Metrics class provides a comprehensive suite of statistical methods to assess the reliability and agreement of ratings across different raters. It supports various scales and measurement types, including ordinal, nominal, and interval scales. The class is designed to handle multiple raters and categories, offering calculations of several inter-rater reliability coefficients such as Cohen's Kappa, Fleiss' Kappa, Gwet's AC, Krippendorff's Alpha, and the Intraclass Correlation Coefficient (ICC). Additionally, it includes methods to compute overall agreement and specific indices like the G index. This class is essential for statistical analysis in fields where agreement measurement is crucial, such as psychology, medical research, and any other domain where qualitative or quantitative assessments are made by multiple observers.
    """

    def __init__(self, scale_format, categories, ratings, weights):
        """
        Initialize the Metrics object with specified parameters for scale format, categories, ratings, and weights.

        This constructor sets up the Metrics object by initializing various properties such as scale format, categories, ratings, and the number of subjects. It also determines the type of analysis to be performed based on the scale format, either using irrCAC for ordinal or nominal scales or using pingouin for other types of scales. Additionally, it sets the decimal precision context.

        Parameters:
            scale_format (str): The format of the scale, e.g., 'ordinal', 'nominal'.
            categories (list): A list of categories applicable to the ratings.
            ratings (DataFrame): A pandas DataFrame containing the ratings data.
            weights (list): A list of weights corresponding to the categories.
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
            Calculate and return the Cohen's Kappa coefficient value for the ratings.

            This method computes the Cohen's Kappa coefficient, a statistical measure of inter-rater reliability
            or agreement for qualitative (categorical) items. It is generally thought to be a more robust measure
            than simple percent agreement calculation, as Kappa takes into account the agreement occurring by chance.

            Returns:
                float: The Cohen's Kappa coefficient value.
            ""\"
        """
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
        Calculates and returns the Krippendorff's alpha coefficient value for inter-rater reliability.

        This method computes the Krippendorff's alpha, a statistical measure of the agreement achieved when coding a set of units based on the level of measurement specified. It is used to assess the reliability of raters (inter-rater reliability).

        Returns:
            float: The Krippendorff's alpha coefficient value rounded to four decimal places.
        """
        return self.analysis.krippendorff()['est']['coefficient_value']

    def g_index(self):
        """
        Calculates the G index, a measure of agreement that adjusts the observed agreement for the probability of chance agreement among categories.

        The G index is computed using the formula:
            G = (P_a - 1/q) / (1 - 1/q)
        where P_a is the overall agreement and q is the number of categories.

        Returns:
            float: The G index rounded to four decimal places.
        """
        q = len(self.categories)
        p_a = self.overall_agreement()
        g_index = (p_a - dec.Decimal('1') / q) / (dec.Decimal('1') - dec.
            Decimal('1') / q)
        return float(round(g_index, 4))

    def icc(self):
        """
        Calculates the Intraclass Correlation Coefficient (ICC) for assessing the reliability of measurements where quantitative measurements are made on units that are organized into groups.

        It constructs a DataFrame from the ratings data, specifying targets, raters, and ratings, and then uses the `pingouin.intraclass_corr` function to compute the ICC, handling missing data according to the specified policy.

        Returns:
            A pandas DataFrame containing the ICC results, rounded to four decimal places.
        """
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
        Calculates the overall agreement among raters for a given set of ratings.

        This method computes the proportion of agreement among raters, adjusted for the number of categories and replications. It supports two scenarios:
        1. When there are exactly two replications, it calculates the proportion of subjects that received the same category rating from both replications.
        2. When there are more than two replications, it calculates the agreement based on a more complex formula that considers all possible pairs of ratings for each subject.

        Returns:
            decimal.Decimal: The overall agreement proportion.

        Raises:
            ValueError: If there are fewer than two replications per subject, making it impossible to calculate an overall agreement.
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
        ""\"
        Maps a human-readable metric name to its corresponding method name in the analysis object.

        Args:
        metric (str): A string representing the name of the metric. This can be one of the following:
                      "Cohen's-|Conger's κ", "Fleiss' κ", "Krippendorff's α", "Gwet's AC".

        Returns:
        str: The method name as a string that corresponds to the given metric.
        ""\"
    """
    if metric == "Cohen's-|Conger's κ":
        return 'conger'
    elif metric == "Fleiss' κ":
        return 'fleiss'
    elif metric == "Krippendorff's α":
        return 'krippendorff'
    elif metric == "Gwet's AC":
        return 'gwet'
