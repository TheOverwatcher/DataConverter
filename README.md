# DataConverter
The Data Converter is meant to convert one type of data to another for ease of making test data or other uses. Currently the Data Converted only supports CSV to JSON.

## Configuration
The configuration file should be named *DataConverter.ini*. The configuration has a few sections oulined below to provide dynamic structure to the JSON from the provided CSV columns. Other configuration data is for logging and debugging.

### App Data and Log Data
These sections contain the app name to define what shows as outputting within the logs. The log_file_path must exist for the converter to run.

### CSV Data
The CSV Data section have two uses: the filename to read and the column information. Configuration names beginning with *Column* will be read in as fields to read in from the csv file provided in the configuration field 'filename'.

### JSON Data
The structure of the JSON being converted to is stored under this section. The name of the JSON object should equal the parent JSON object. *None* should be used if there is no parent object. For best results use unique names for each JSON object.

## Output
The resulting file is output as the beginning of the CSV filename, but in JSON. The CSV file can have many row for each column and will be combined into a list of that information in the JSON output.