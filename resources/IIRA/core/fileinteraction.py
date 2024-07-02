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
    The `FileValidation` class is designed to handle and validate data from various file formats, primarily focusing on Excel and CSV files. It provides functionality to initialize data processing based on file content and specified scale formats (nominal or ordinal), determine file formats, extract and process unique categories, rater IDs, and text data, and organize labels according to the data format and scale format. Additionally, the class supports writing processed data to files, generating unique identifiers for users, and formatting text data for further analysis. This class is essential for applications requiring detailed data validation and processing, ensuring data integrity and proper formatting for analytical purposes.
    """

    def __init__(self, file, scale_format):
        """
            ""\"
            Initialize the FileValidation instance with a specified file and scale format.

            This method sets up the initial state by determining the file type (Excel or CSV),
            reading the file content, and initializing various attributes used for data processing.
            It also performs initial checks and data extraction based on the file content and
            specified scale format (nominal or ordinal).

            Parameters:
                file (str): The path to the file containing the data to be validated.
                scale_format (str): The scale format of the data, which can be 'nominal' or 'ordinal'.
            ""\"
        """
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
        Determines the format of the data file based on the column headers.

        This method checks the column headers of the data file loaded into the `content` DataFrame.
        It sets the `format` attribute of the class to "Format 1" if the header "Rater ID" is found,
        or to "Format 2" if the header "Subject" is found. If neither header is present, it raises a ValueError.

        Raises:
            ValueError: If neither "Rater ID" nor "Subject" headers are found in the columns.
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
            ""\"
            Extracts unique categories from the 'Categories' column of the content DataFrame.

            This method iterates over each item in the 'Categories' column of the DataFrame stored in self.content.
            It appends each non-null and unique category to the self.categories list attribute of the class.
            ""\"
        """
        for item in self.content['Categories']:
            if not pd.isnull(item):
                self.categories.append(item)

    def find_rater_ids(self):
        """
            ""\"
            Identifies and stores unique rater IDs from the dataset based on the specified format.

            This method checks the format of the dataset and extracts rater IDs accordingly.
            If the format is "Format 1", it extracts IDs from the "Rater ID" column.
            If the format is "Format 2", it identifies headers that are not "Subject" and considers them as rater IDs.
            Additionally, if the scale format is "nominal" or "ordinal", it further filters these headers to include only those that match the predefined categories.
            ""\"
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
            Extracts and processes text data from the content based on the specified format and scale format.

            This method identifies and extracts text data from the loaded content, applying different logic
            based on the current format ('Format 1' or 'Format 2') and scale format ('nominal' or 'ordinal').
            The extracted text is then processed using the `nlp` method to format it appropriately.

            For 'Format 1':
                - If the scale format is 'nominal' or 'ordinal', it extracts headers that are not in the
                  categories or rater IDs and processes them.
                - Otherwise, it processes all headers except 'Rater ID'.
            For 'Format 2':
                - It processes the 'Subject' column values.

            The processed text is stored in `self.text` and the formatted version in `self.formatted_text`.
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
        Extracts and organizes labels from the dataset based on the specified format and scale format.

        This method processes the dataset to associate text entries with their corresponding labels based on the rater's ID.
        It handles two different data formats:
        - Format 1: Assumes a direct mapping between 'Rater ID' and text entries.
        - Format 2: Uses 'Subject' as a key to map raters to their ratings.

        The labels are stored in a dictionary where each key is a rater's ID and the value is a list of tuples.
        Each tuple contains a formatted text entry and its associated label as rated by the rater.
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
            ""\"
            Writes the combined data of old and new ratings to a file specified by the path.

            This method processes the ratings provided, combines them with existing data,
            and writes the result to a file. The file format is determined by the file extension
            in the path. Supported formats include .xlsx, .xls, .ods, and CSV.

            Parameters:
            - path (str): The file path where the data will be written. The file extension determines the format.
            - ratings (list of tuples): A list of tuples, where each tuple contains the profile and rating.

            The method handles different data formats and scale formats, and it appends a timestamp to new entries.
            ""\"
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
            ""\"
            Generate a unique identifier for a user by prefixing a given username with 'ir_app_'.

            Parameters:
                user (str): The username for which the identifier will be generated.

            Returns:
                str: A unique identifier for the user.
            ""\"
        """
        return 'ir_app_' + user

    def nlp(self, text):
        """
            ""\"
            Process and format the input text by extracting the most relevant content within brackets and removing numeric suffixes.

            This method is specifically designed to handle text that includes metadata about sentence polarity. It extracts the
            main content within brackets and removes any trailing numeric suffixes from the text, which are often present in
            structured or semi-structured data formats.

            Parameters:
            - text (str): The text to be processed, which may include metadata and numeric suffixes.

            Returns:
            - str: The processed text with relevant content extracted and numeric suffixes removed.
            ""\"
        """
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
    A class designed to manage and interact with database profiles, specifically for handling user profiles within a database system. This class provides functionality to initialize the database interaction, load profiles, create new profiles, delete profiles, switch between profiles, and write changes back to the database.

    The class supports operations such as initializing with a specific file and format, loading existing profiles from the database, creating new profiles and setting them as active, deleting the current active profile, changing the active profile, and persistently saving profile changes to the database.
    """

    def __init__(self, db_path):
        """
            ""\"
            Initialize the FileValidation instance with a specified file and scale format.

            This method sets up the initial state by determining the file type (Excel or CSV),
            reading the file content, and initializing various attributes used for data processing.
            It also performs initial checks and data extraction based on the file content and
            specified scale format (nominal or ordinal).

            Parameters:
                file (str): The path to the file containing the data to be validated.
                scale_format (str): The scale format of the data, which can be 'nominal' or 'ordinal'.
            ""\"
        """
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
            Load profiles from the database into the instance.

            This method initializes the active profile and loads additional profiles from the database.
            If the database contains profiles, the first profile is set as the active profile and the rest are loaded into the profiles list.
            If there are no profiles in the database, the method returns without making any changes.
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
            Creates a new profile and updates the active profile to the newly created one.

            This method appends the current active profile to the list of profiles if it is not empty,
            then sets the new profile as the active profile and updates the database with the new profile information.

            Parameters:
            - new_profile (str): The name of the new profile to be created and set as active.

            Returns:
            None
            ""\"
        """
        if self.active_profile != '':
            self.profiles.append(self.active_profile)
        self.active_profile = new_profile
        self.write_to_db()

    def delete_profile(self):
        """
        Deletes the currently active profile from the database, making the first profile in the list the new active profile. Updates the database accordingly.
        """
        self.active_profile = self.profiles[0]
        self.profiles.remove(self.active_profile)
        self.write_to_db()

    def change_profile(self, change_to):
        """
        Switches the active profile to a specified profile and updates the database accordingly.

        This method changes the currently active profile to the one specified by the 'change_to' parameter.
        It also updates the list of profiles by moving the newly activated profile to the active position
        and appending the previously active profile to the list of other profiles. After changing the profile,
        it calls `write_to_db` to save the changes to the database.

        Parameters:
            change_to (str): The profile name to which the active profile should be changed.

        Returns:
            None
        """
        tmp = self.active_profile
        self.active_profile = change_to
        self.profiles.remove(change_to)
        self.profiles.append(tmp)
        self.write_to_db()

    def write_to_db(self):
        """
            ""\"
            Writes the current profile data to the database file.

            This method updates the database file by writing the active profile and the list of other profiles
            into a DataFrame and then saving it to the specified database path in CSV format.
            ""\"
        """
        self.db = pd.DataFrame([self.active_profile] + self.profiles,
            columns=['Profile'])
        self.db.to_csv(self.db_path, sep=';', index=False, header=True)


def write_excel(analyse, intra_ids, intra_metrics, inter_ids, inter_metrics,
    scale_format, filename):
    """
        ""\"
        Generates an Excel file with intra-rater and inter-rater analysis results.

        This function creates an Excel workbook that includes detailed statistical analysis results
        for both intra-rater and inter-rater evaluations based on provided metrics and IDs. The workbook
        contains multiple sections formatted for clarity and ease of understanding, including bold headers
        and structured data presentation.

        Parameters:
            analyse (Analysis): An object containing the analysis results.
            intra_ids (list): List of IDs for intra-rater analysis.
            intra_metrics (list): List of metrics to be reported for intra-rater analysis.
            inter_ids (list): List of IDs for inter-rater analysis.
            inter_metrics (list): List of metrics to be reported for inter-rater analysis.
            scale_format (str): The scale format of the ratings ('nominal', 'ordinal', etc.).
            filename (str): The path to the file where the Excel workbook will be saved.

        Returns:
            None: The function writes directly to an Excel file specified by `filename`.
        ""\"
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
