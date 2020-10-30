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

        print(self.json_structure)

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

        """
        try:
            with open(self.filename) as csvfile:
                all_data = csv.DictReader(csvfile, delimiter=',')

                json_array = None
                for row in all_data:
                    record = self.build_record(row)

                    formatted_record = self.format_record(record)

                    # print(json_array)
                    if json_array is not None:
                        combine = json_array[0]
                        for key in combine:
                            # print(key)
                            combine[key].append(formatted_record[key][0])
                            # print(formatted_record[key][0])
                    else:
                        json_array = []
                        json_array.append(formatted_record)

                final_json = json.dumps(json_array)
                # print("This is it boys and girls")
                # print(final_json)
                f = open(self.filename[:-4] + '.json', 'w')
                f.write(final_json)

        except IOError as err:
            self.log("INFO", "Failure opening file: " + self.filename)

    def format_record(self, record):
        # Loop through the record and place values of keys that exist
        # within the json_structure
        # print("After formatting:")
        # print(self.json_structure)
        print(record)

        new_dict = {}
        for key in self.json_structure:
            # print("Processing key: " + key)
            if self.json_structure[key] is not None:
                # print("Recursive return: ")
                ret = self.recursive_search(self.json_structure[key], record)
                new_dict[key] = ret
            else:
                print("passing")
                # Check if an item in the columns is this key
                # Since it has no value
                pass

        # print("After formatting: ")
        # print(new_dict)
        return new_dict

    def build_record(self, row):
        assert row, "Missing parameter!"

        record = {}

        for col in self.columns:
            record[col] = row[col]

        # for column in self.columns:
        # self.log("INFO", record)

        return record

    def recursive_search(self, structure, record):
        # print(structure)

        if not type(structure) == list:
            return
        else:
            # print("Before: ")
            # print(structure)
            new_dict = {}
            for obj in structure:
                # print(obj)
                self.recursive_search(obj, record)
                # print(structure.index(obj))
                # print(structure[structure.index(obj)])
                # structure[structure.index(obj)] = \
                # print(self.replace_with_column_data(obj, record))
                for item in self.columns:
                    # print("Item: " + item)
                    # print("Key: " + key)
                    if obj == item:
                        # print(structure)
                        # print(structure[structure.index(obj)])
                        new_dict[item] = record[item]
                        # print(structure)

            structure = [new_dict]

            # print("After: ")
            # print(structure)

        return structure

    def replace_with_column_data(self, key, record):
        for item in self.columns:
            # print("Item: " + item)
            # print("Key: " + key)
            if key == item:
                return {key: record[key]}
