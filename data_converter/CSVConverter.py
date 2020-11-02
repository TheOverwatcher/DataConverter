import csv
import json
import copy
import logging


class CSVConverter():
    def __init__(self, config_data):
        self.app_data = config_data['APP_DATA']
        self.app_data.__len__

        # CSV configuration to read
        self.csv_data = config_data['CSV_DATA']
        self.filename = self.csv_data['FILENAME']
        self.columns = []
        for col in self.csv_data:
            if col.startswith("COLUMN"):
                self.columns.append(self.csv_data[col.upper()])

        # Json Configuration to write
        self.json_data = config_data['JSON_DATA']
        self.json_structure = {}
        for jobject in self.json_data:
            parent = self.json_data[jobject]
            self.find_forefathers(jobject, parent)

        # Setup logging
        self.logger_name = self.app_data['APP_NAME']
        self.logger = logging.getLogger(self.logger_name)
        assert self.logger, "Failed to establish our logger instance!"

    def find_forefathers(self, child, parent):
        """ Recursive method to add an unordered set to a structured object.

            The configuration of the json object will be unsorted when read in.
            This method is a recursive implementation to find a decendent's
            forefathers and add them to a structured object so KeyErrors don't
            occur. A child is the 'key' and the parent is the 'value'.
        """
        # We found the most parent object
        if parent == 'None':
            return
        else:
            self.find_forefathers(parent, self.json_data[parent.upper()])

        if parent not in self.json_structure:
            self.json_structure[parent] = []

        self.json_structure[parent].append(child.lower())

        return

    def log(self, log_level, log_msg):
        """
            Generic method to handle log entries.
        """
        if('DEBUG' == log_level):
            self.logger.debug(log_msg)
        elif('INFO' == log_level):
            self.logger.info(log_msg)
        elif 'WARNING' == log_level:
            self.logger.warning(log_msg)
        elif 'ERROR' == log_level:
            self.logger.error(log_msg)
        elif 'CRITICAL' == log_level:
            self.logger.critical(log_msg)
        else:
            assert log_level, "Invalid log level"

        return

    def convert_data(self):
        """ Method containing the full process of conversion.

            First we read the file in the same directory. For every row in the
            CSV we make a record then format the record in the structure of the
            JSON. Then each formatted record is appended to an array and
            combined with like JSON objects to build the objects properly.
            Lastly we write the JSON to a file named after the CSV file.
        """
        self.log("Attempting to convert " + self.filename + " to JSON.")
        try:
            with open(self.filename) as csvfile:
                all_data = csv.DictReader(csvfile, delimiter=',')

                json_array = None
                for row in all_data:
                    record = self.build_record(row)

                    formatted_record = self.format_record(record)

                    if json_array is not None:
                        combine = json_array[0]
                        for key in combine:
                            combine[key].append(formatted_record[key][0])
                    else:
                        json_array = []
                        json_array.append(formatted_record)

                final_json = json.dumps(json_array[0])
                json_filename = self.filename[:-4] + '.json'
                f = open(json_filename, 'w')
                f.write(final_json)

        except IOError as err:
            self.log("ERROR", "Failure opening file: " + self.filename)

        self.log("Conversion complete. See " + json_filename + " for output.")

    def format_record(self, record):
        """ Format the record from the CSV into the structure of the JSON.

            Match the JSON objects to the CSV columns and input the data from
            the record into a JSON formatted record.
        """

        new_dict = {}
        for key in self.json_structure:
            if self.json_structure[key] is not None:
                ret = self.recursive_search(self.json_structure[key], record)
                new_dict[key] = ret
            else:
                print("passing")
                pass

        return new_dict

    def build_record(self, row):
        """ Build a record from a row in the CSV data.
        """
        assert row, "Missing parameter!"

        record = {}

        for col in self.columns:
            record[col] = row[col]

        return record

    def recursive_search(self, structure, record):
        """ Method to search through the modified structure to add indexes in
            case of a KeyError.

            Recursive function meant to prevent KeyErrors when adding record
            information to an dictionary when the parent records in the JSON
            have yet to be added. If the parent wasn't found, add it and all
            ancestry based on the JSON structure provided in the configuration.
        """

        if not type(structure) == list:
            return
        else:
            new_dict = {}
            for obj in structure:
                self.recursive_search(obj, record)
                for item in self.columns:
                    if obj == item:
                        new_dict[item] = record[item]

            structure = [new_dict]

        return structure
