import re
import pathlib
import datetime
from math import isnan
import pandas as pd
import numpy as np
import xlsxwriter
from pprint import pprint
from core.metrics import map_metrics
PROFILE = 0
RATING = 1


class FileValidation:
    """
    The FileValidation class is designed to validate and process file content based on specific formats and scale formats. It reads the file into a pandas DataFrame, determines the file format, and extracts relevant information such as categories, rater IDs, text, and labels. The class also provides functionality to write the processed content back to a file and to perform text processing and user identifier conversion.

    Attributes:
        debug (bool): A flag for debugging mode.
        content (DataFrame): The content of the file read into a pandas DataFrame.
        format (str): The format of the file, determined by its headers.
        scale_format (str): The scale format of the data.
        categories (list): A list of categories found in the file.
        rater_ids (list): A list of rater IDs found in the file.
        text (list): A list of text headers or subjects found in the file.
        formatted_text (list): A list of formatted text headers or subjects.
        labels (dict): A dictionary mapping rater IDs to their corresponding labels.

    Raises:
        ValueError: If the file format is not recognized or if the file content does not contain the required headers to determine the format.
        KeyError: If the 'Categories' column is not present in the DataFrame.
    """

    def __init__(self, file, scale_format):
        self.debug = False
        file_extension = pathlib.Path(file).suffix
        self.content = None
        self.format = None
        self.scale_format = scale_format
        self.categories = []
        self.rater_ids = []
        self.text = []
        self.formatted_text = []
        self.labels = {}
        if file_extension == '.xlsx' or file_extension == '.xls':
            self.content = pd.read_excel(file)
        elif file_extension == '.ods':
            self.content = pd.read_excel(file, engine='odf')
        else:
            self.content = pd.read_csv(file, delimiter=';')
        self.content = self.content.loc[:, ~self.content.columns.str.
            contains('^Unnamed')]
        self.check_format()
        if self.scale_format == 'nominal' or self.scale_format == 'ordinal':
            self.find_categories()
        self.find_rater_ids()
        self.find_text()
        self.find_labels()
        if self.debug:
            print('Format:')
            print(self.format)
            print('Scale Format:')
            print(self.scale_format)
            print('Categories:')
            print(self.categories)
            print("Rater ID's:")
            print(self.rater_ids)
            print()
            print('Text:')
            print(self.text)
            print()
            print('Formatted Text')
            print(self.formatted_text)
            print()
            print('Labels')
            print(self.labels)
            print()

    def check_format(self):
        """
        Determine the format of the file content based on its headers.

        This method inspects the headers of the file content to identify the format.
        It sets the `format` attribute to "Format 1" if a header named "Rater ID" is found,
        or to "Format 2" if a header named "Subject" is found. If neither header is found,
        a `ValueError` is raised.

        Raises:
            ValueError: If the file content does not contain the required headers to determine the format.
        """
        headers = list(self.content.columns)
        for header in headers:
            header = header.lower()
            if header == 'Rater ID'.lower():
                self.format = 'Format 1'
                return
            if header == 'Subject'.lower():
                self.format = 'Format 2'
                return
        raise ValueError

    def find_categories(self):
        """
        Extracts and stores the categories from the 'Categories' column of the content DataFrame.

        This method iterates through the 'Categories' column of the DataFrame stored in the `content` attribute.
        For each non-null item in the column, it appends the item to the `categories` attribute list.

        Raises:
            KeyError: If the 'Categories' column is not present in the DataFrame.
        """
        for item in self.content['Categories']:
            if not pd.isnull(item):
                self.categories.append(item)

    def find_rater_ids(self):
        """
        Extracts and stores unique rater IDs from the content based on the file format and scale format.

        For "Format 1", it collects unique rater IDs from the "Rater ID" column.
        For "Format 2", it collects column headers as rater IDs based on the scale format:
        - For "nominal" or "ordinal" scale formats, it collects headers where all values are in the categories list or are null.
        - For other scale formats, it collects all headers except "Subject".

        Raises:
            ValueError: If the format is not recognized.
        """
        if self.format == 'Format 1':
            for item in self.content['Rater ID']:
                if not pd.isnull(item):
                    if item not in self.rater_ids:
                        self.rater_ids.append(item)
        elif self.format == 'Format 2':
            if (self.scale_format == 'nominal' or self.scale_format ==
                'ordinal'):
                for header in self.content:
                    if all(self.content[header].isin(self.categories) |
                        self.content[header].isnull()):
                        if header not in self.rater_ids:
                            self.rater_ids.append(header)
            else:
                for header in self.content:
                    if header == 'Subject':
                        continue
                    if header not in self.rater_ids:
                        self.rater_ids.append(header)

    def find_text(self):
        """
        ""\"
        Extracts and processes text data from the content based on the file format and scale format.

        For 'Format 1':
        - If the scale format is 'nominal' or 'ordinal', it identifies headers that match the categories and processes them.
        - Otherwise, it processes all headers except 'Rater ID'.

        For 'Format 2':
        - It processes all non-null items in the 'Subject' column.

        The processed text is stored in the `text` and `formatted_text` attributes.

        Raises:
        - None
        ""\"
        """
        if self.format == 'Format 1':
            if (self.scale_format == 'nominal' or self.scale_format ==
                'ordinal'):
                for header in self.content:
                    if self.debug:
                        print('header: ' + str(header))
                    if all(self.content[header].isin(self.categories) |
                        self.content[header].isnull()):
                        if header not in self.rater_ids:
                            if 'Categories' == header:
                                continue
                            self.formatted_text.append(self.nlp(header))
                            self.text.append(header)
            else:
                for header in self.content:
                    if header == 'Rater ID':
                        continue
                    self.formatted_text.append(self.nlp(header))
                    self.text.append(header)
        elif self.format == 'Format 2':
            for item in self.content['Subject']:
                if not pd.isnull(item):
                    self.formatted_text.append(self.nlp(item))
                    self.text.append(item)

    def find_labels(self):
        """
        Extracts and organizes labels from the content based on the file format and scale format.

        For 'Format 1', it iterates through each row, associating text labels with their corresponding rater IDs.
        For 'Format 2', it associates text labels with rater IDs by iterating through the subjects.

        Raises:
            ValueError: If the format is not recognized.

        """
        if self.format == 'Format 1':
            for row in range(len(self.content)):
                if pd.isnull(self.content.loc[row, 'Rater ID']):
                    continue
                text_label_list = []
                for i, text in enumerate(self.text):
                    text_label_list.append((self.formatted_text[i], self.
                        content.loc[row, text]))
                if self.content.loc[row, 'Rater ID'] in self.labels:
                    self.labels[self.content.loc[row, 'Rater ID']
                        ] += text_label_list
                else:
                    self.labels[self.content.loc[row, 'Rater ID']
                        ] = text_label_list
        elif self.format == 'Format 2':
            for rater_id in self.rater_ids:
                text_label_list = []
                for row in range(len(self.content)):
                    if pd.isnull(self.content.loc[row, 'Subject']):
                        continue
                    text_label_list.append((self.content.loc[row, 'Subject'
                        ], self.content.loc[row, rater_id]))
                if rater_id in self.labels:
                    self.labels[rater_id] += text_label_list
                else:
                    self.labels[rater_id] = text_label_list

    def write_file(self, path, ratings):
        """
        Write the content of the DataFrame to a file.

        Parameters:
        path (str): The file path where the DataFrame should be written.
        ratings (list of tuples): A list of tuples where each tuple contains a profile and its corresponding rating.

        Raises:
        ValueError: If the file extension is not supported.
        """
        if self.scale_format == 'nominal' or self.scale_format == 'ordinal':
            columns = ['Categories', 'Rater ID']
        else:
            columns = ['Rater ID']
        users = []
        col_rename = {}
        if self.format == 'Format 1':
            for txt in self.text:
                columns.append(txt)
                col_rename[txt] = self.nlp(txt)
        else:
            pass
        for rating in ratings:
            if rating == ():
                continue
            if rating[PROFILE] not in users:
                users.append(rating[PROFILE])
        old_df = pd.DataFrame(self.content, columns=columns)
        old_df = old_df.rename(columns=col_rename)
        if self.debug:
            print('old df')
            print(old_df)
            print()
        if self.scale_format == 'nominal' or self.scale_format == 'ordinal':
            columns = ['Categories', 'Rater ID']
        else:
            columns = ['Rater ID']
        for txt in self.formatted_text:
            columns.append(txt)
        new_df = pd.DataFrame([], columns=columns)
        for user in users:
            if (self.scale_format == 'nominal' or self.scale_format ==
                'ordinal'):
                row = [np.nan, self.usr_to_id(user)]
            else:
                row = [self.usr_to_id(user)]
            for rating in ratings:
                if rating == ():
                    row.append(np.nan)
                elif rating[PROFILE] == user:
                    row.append(rating[RATING])
                else:
                    row.append(np.nan)
            new_df.loc[len(new_df)] = row
        df = pd.concat([old_df, new_df], axis='index')
        df = df.reset_index(drop=True)
        current_datetime = datetime.datetime.now()
        current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        date_col = []
        for i in range(len(old_df)):
            date_col.append(np.nan)
        for i in range(len(new_df)):
            date_col.append(current_datetime)
        date_df = pd.DataFrame({'datum_ir_app': date_col})
        df = pd.concat([df, date_df], axis='columns')
        file_extension = pathlib.Path(path).suffix
        if file_extension == '.xlsx' or file_extension == '.xls':
            df.to_excel(path, index=False, header=True)
        elif file_extension == '.ods':
            df.to_excel(path, engine='odf', index=False, header=True)
        else:
            df.to_csv(path, sep=';', index=False, header=True)

    def usr_to_id(self, user):
        """
        Convert a user identifier to a standardized format.

        Args:
            user (str): The user identifier to be converted.

        Returns:
            str: The standardized user identifier prefixed with 'ir_app_'.
        """
        return 'ir_app_' + user

    def nlp(self, text):
        sentisurvey_metadata = (
            'How would you label the following sentences regarding its polarity? Rate the sentences as positive, negative or neutral (neither positive nor negative) based on your perception.'
            )
        if sentisurvey_metadata in text:
            text = max(re.findall(re.escape('[') + '(.*?)' + re.escape(']'),
                text), key=len)
        text = re.sub('\\.[0-9]*$', '', text)
        return text


class DBInteraction:
    """
    DBInteraction class for managing user profiles in a database.

    This class provides methods to load, create, delete, change, and write user profiles to a database file. It ensures that the profiles are managed efficiently and consistently, with the ability to handle various exceptions that may arise during these operations.

    Attributes:
        active_profile (str): The currently active profile.
        profiles (list): A list of all profiles.
        db_file (str): The path to the database file.

    Methods:
        load_profiles: Loads profiles from the database file into the class instance.
        create_profile: Creates a new profile and sets it as the active profile.
        delete_profile: Deletes the currently active profile and sets the next profile in the list as active.
        change_profile: Changes the active profile to the specified profile.
        write_to_db: Writes the current profiles to the database file.
    """

    def __init__(self, db_path):
        file_extension = pathlib.Path(db_path).suffix
        self.db_path = db_path
        self.db = None
        self.active_profile = ''
        self.profiles = []
        if file_extension == '.xlsx' or file_extension == '.xls':
            self.db = pd.read_excel(db_path)
        elif file_extension == '.ods':
            self.db = pd.read_excel(db_path, engine='odf')
        else:
            self.db = pd.read_csv(db_path, delimiter=';')
        self.load_profiles()

    def load_profiles(self):
        """
        ""\"
        Loads profiles from the database file into the class instance.

        This method checks if the "Profile" column in the database file is not empty.
        If the first entry in the "Profile" column is not null, it sets the first entry
        as the active profile and the rest of the entries as the list of profiles.

        Returns:
            None
        ""\"
        """
        if len(self.db['Profile']) > 0:
            if not pd.isnull(self.db['Profile'][0]):
                self.active_profile = self.db['Profile'][0]
                self.profiles = list(self.db['Profile'][1:])
        else:
            return

    def create_profile(self, new_profile):
        """
        ""\"
        Create a new profile and set it as the active profile.

        If there is already an active profile, it will be added to the list of profiles.
        The new profile will then be set as the active profile and the database will be updated.

        Args:
            new_profile (str): The name of the new profile to be created.
        ""\"
        """
        if self.active_profile != '':
            self.profiles.append(self.active_profile)
        self.active_profile = new_profile
        self.write_to_db()

    def delete_profile(self):
        """
        Deletes the currently active profile and sets the next profile in the list as active.

        This method updates the active profile to the first profile in the profiles list,
        removes the newly active profile from the profiles list, and writes the updated
        profiles list to the database.

        Raises:
            IndexError: If there are no profiles available to set as active.
        """
        self.active_profile = self.profiles[0]
        self.profiles.remove(self.active_profile)
        self.write_to_db()

    def change_profile(self, change_to):
        """
        Change the active profile to the specified profile.

        Args:
            change_to (str): The profile to switch to.

        Raises:
            ValueError: If the specified profile does not exist in the profiles list.
        """
        tmp = self.active_profile
        self.active_profile = change_to
        self.profiles.remove(change_to)
        self.profiles.append(tmp)
        self.write_to_db()

    def write_to_db(self):
        """
        ""\"
        Writes the current profiles to the database file.

        This method updates the database file with the current active profile and the list of profiles.
        The data is saved in a CSV format with a single column named "Profile".

        Raises:
            IOError: If there is an issue writing to the database file.
        ""\"
        """
        self.db = pd.DataFrame([self.active_profile] + self.profiles,
            columns=['Profile'])
        self.db.to_csv(self.db_path, sep=';', index=False, header=True)


def write_excel(analyse, intra_ids, intra_metrics, inter_ids, inter_metrics,
    scale_format, filename):
    """
    Generate an Excel report for intra-rater and inter-rater analysis results.

    Args:
        analyse (object): An object containing the analysis results.
        intra_ids (list): List of rater IDs for intra-rater analysis.
        intra_metrics (list): List of metrics for intra-rater analysis.
        inter_ids (list): List of rater IDs for inter-rater analysis.
        inter_metrics (list): List of metrics for inter-rater analysis.
        scale_format (str): The scale format, either "nominal" or "ordinal".
        filename (str): The name of the output Excel file.

    Raises:
        ZeroDivisionError: If a division by zero occurs during metric calculation.
    """
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    b_cell_format = workbook.add_format()
    b_cell_format.set_bold()
    not_enough_ratings = []
    if scale_format == 'nominal' or scale_format == 'ordinal':
        if intra_ids and intra_metrics:
            worksheet.write(0, 0, 'Intra-Rater-Analyse', b_cell_format)
            worksheet.write(1, 0, '')
            worksheet.write(2, 0, 'Gewichte', b_cell_format)
            worksheet.write(3, 0, analyse.results['intra'][intra_ids[0]].
                weights_name)
            worksheet.write(4, 0, '')
            worksheet.write(5, 0, '')
            worksheet.write(6, 0, 'Rater ID', b_cell_format)
            worksheet.write(6, 1, '#Subjects', b_cell_format)
            worksheet.write(6, 2, '#Replicates', b_cell_format)
            j = 3
            for metric in intra_metrics:
                worksheet.write(6, j, metric, b_cell_format)
                j += 1
            i = 7
            for rater_id in intra_ids:
                quant_subjects = analyse.results['intra'][rater_id].n
                quant_replicates = analyse.results['intra'][rater_id].r
                if quant_replicates < 2 or quant_subjects < 1:
                    not_enough_ratings.append(str(rater_id))
                    continue
                worksheet.write(i, 0, rater_id)
                worksheet.write(i, 1, quant_subjects)
                worksheet.write(i, 2, quant_replicates)
                j = 3
                cont = False
                for metric in intra_metrics:
                    metric_function_name = map_metrics(metric)
                    try:
                        metric_dict = getattr(analyse.results['intra'][
                            rater_id], metric_function_name)()['est']
                        metric_value = metric_dict['coefficient_value']
                        if isnan(metric_value
                            ) and metric == "Cohen's-|Conger's κ":
                            metric_value = 1.0
                        worksheet.write(i, j, str(metric_value))
                    except ZeroDivisionError:
                        worksheet.write(i, j, '1.0')
                    j += 1
                if cont:
                    continue
                i += 1
            worksheet.write(i, 0, '')
            worksheet.write(i + 1, 0, '')
            i += 2
            for rater_id in intra_ids:
                quant_subjects = analyse.results['intra'][rater_id].n
                quant_replicates = analyse.results['intra'][rater_id].r
                if quant_replicates < 2 or quant_subjects < 1:
                    continue
                worksheet.write(i, 0, 'Rater ID', b_cell_format)
                worksheet.write(i + 1, 0, rater_id)
                worksheet.write(i, 1, '#Subjects', b_cell_format)
                worksheet.write(i + 1, 1, quant_subjects)
                worksheet.write(i, 2, '#Replikate', b_cell_format)
                worksheet.write(i + 1, 2, quant_replicates)
                worksheet.write(i + 2, 0, '')
                i = i + 3
                for metric in intra_metrics:
                    metric_function_name = map_metrics(metric)
                    try:
                        metric_dict = getattr(analyse.results['intra'][
                            rater_id], metric_function_name)()['est']
                        worksheet.write(i, 0, metric, b_cell_format)
                        worksheet.write(i + 1, 0, str(metric_dict[
                            'coefficient_value']))
                        worksheet.write(i, 1, 'p-Wert', b_cell_format)
                        worksheet.write(i + 1, 1, str(metric_dict['p_value']))
                        worksheet.write(i, 2, '95% Konfidenzintervall',
                            b_cell_format)
                        worksheet.write(i + 1, 2, str(metric_dict[
                            'confidence_interval']))
                        worksheet.write(i + 2, 0, '')
                    except ZeroDivisionError:
                        worksheet.write(i, 0, metric, b_cell_format)
                        worksheet.write(i + 1, 0, '1.0')
                        worksheet.write(i, 1, 'p-Wert', b_cell_format)
                        worksheet.write(i + 1, 1, 'n.a.')
                        worksheet.write(i, 2, '95% Konfidenzintervall',
                            b_cell_format)
                        worksheet.write(i + 1, 2, '(n.a., n.a.)')
                        worksheet.write(i + 2, 0, '')
                    i = i + 3
            worksheet.write(i, 0, '')
            worksheet.write(i + 1, 0, '')
            worksheet.write(i + 2, 0, '')
            worksheet.write(i + 3, 0,
                "ID's, die kein Subject mehrfach bewertet haben:")
            i = i + 4
            for id in not_enough_ratings:
                worksheet.write(i, 0, id)
                i += 1
        else:
            i = 0
        if inter_ids and inter_metrics:
            quant_subjects = analyse.results['inter'].n
            quant_raters = analyse.results['inter'].r
            worksheet.write(i, 0, 'Inter-Rater-Analyse', b_cell_format)
            worksheet.write(i + 1, 0, '')
            worksheet.write(i + 2, 0, 'Gewichte', b_cell_format)
            worksheet.write(i + 3, 0, analyse.results['inter'].weights_name)
            worksheet.write(i + 4, 0, '')
            worksheet.write(i + 5, 0, "Rater ID's", b_cell_format)
            worksheet.write(i + 5, 1, '#Subjects', b_cell_format)
            worksheet.write(i + 5, 2, '#Raters', b_cell_format)
            worksheet.write(i + 6, 1, str(quant_subjects))
            worksheet.write(i + 6, 2, str(quant_raters))
            i = i + 6
            for rater_id in inter_ids:
                worksheet.write(i, 0, rater_id)
                i = i + 1
            worksheet.write(i, 0, '')
            i = i + 1
            for metric in inter_metrics:
                metric_function_name = map_metrics(metric)
                metric_dict = getattr(analyse.results['inter'],
                    metric_function_name)()['est']
                worksheet.write(i, 0, metric, b_cell_format)
                worksheet.write(i + 1, 0, str(metric_dict['coefficient_value'])
                    )
                worksheet.write(i, 1, 'p-Wert', b_cell_format)
                worksheet.write(i + 1, 1, str(metric_dict['p_value']))
                worksheet.write(i, 2, '95% Konfidenzintervall', b_cell_format)
                worksheet.write(i + 1, 2, str(metric_dict[
                    'confidence_interval']))
                worksheet.write(i + 2, 0, '')
                i = i + 3
    workbook.close()
