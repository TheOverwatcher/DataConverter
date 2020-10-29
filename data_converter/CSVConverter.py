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
            print(parent)
            print(jobject)
            if parent == 'None':
                if parent not in self.json_structure:
                    self.json_structure[jobject.lower()] = []
            else:
                self.find_forefathers(jobject, parent)
                # self.json_structure[jobject].append(parent)

            print(self.json_structure)

        # Setup logging
        self.logger_name = self.app_data['APP_NAME']
        self.logger = logging.getLogger(self.logger_name)
        assert self.logger, "Failed to establish our logger instance!"

    # Recursive function add forefathers to an array before indexing
    def find_forefathers(self, child, parent):
        print(parent)
        print(child)
        # We found the most parent object
        if parent == 'None':
            return
        else:
            # nextParent = self.json_data[parent.upper()]
            self.find_forefathers(parent, self.json_data[parent.upper()])

        if parent not in self.json_structure:
            self.json_structure[parent] = []
        else:
            self.json_structure[parent].append(child)

        return

    def record_structure(self):
        return copy.deepcopy(self.record_structure)

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

    def convertData(self):
        try:
            with open(self.filename) as csvfile:
                all_data = csv.DictReader(csvfile, delimiter=',')

                structure = None  # self.record_structure()

                for row in all_data:
                    record = self.build_record(row, structure)

        except IOError as err:
            self.log("INFO", "Failure opening file: " + self.filename)

    def build_record(self, row, record_structure):
        assert row, "Missing parameter!"

        record = {}

        for col in self.columns:
            record[col] = row[col]

        # for column in self.columns:
        self.log("INFO", record)

        return record
