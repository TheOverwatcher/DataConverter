from CSVConverter import CSVConverter
import sys
import logging
import logging.handlers
sys.path.append("./lib")
import utilities as Utils  # noqa pylint: disable=import-error


CONFIG_FILE = "DataConverter.ini"


def setup_log_system(config_data):
    """
    """
    assert config_data, "Missing parameter!"
    log_config = config_data['LOG_DATA']
    assert log_config, "Missing LOG config data!"

    logger = logging.getLogger(config_data['APP_DATA']['APP_NAME'])
    logger.setLevel(logging.DEBUG)

    # Create file handler.
    file_path_name = log_config['LOG_FILE_PATH'] +\
        log_config['LOG_FILE']
    log_size = int(log_config['LOG_FILE_MAX_SIZE'])
    num_backups = int(log_config['LOG_FILE_BACKUP_COUNT'])
    fh = logging.handlers.RotatingFileHandler(file_path_name,
                                              maxBytes=log_size,
                                              backupCount=num_backups)

    fh.setLevel(logging.INFO)

    # Create console handler.
    # Commnet out for non-dev operation.
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create formatter and add it to the handlers.
    formatStr = '%(asctime)s - %(name)s:%(levelname)s - %(message)s'
    formatter = logging.Formatter(formatStr)
    fh.setFormatter(formatter)

    # Commnet out for non-dev operation.
    ch.setFormatter(formatter)

    # Add the handlers to the logger.
    logger.addHandler(fh)

    # Commnet out for non-dev operation.
    logger.addHandler(ch)

    logger = None
    return logger


def usage_help():
    """
    """
    print("This script will perform a data conversion between CSV and JSON.\n")
    print("Usage: python DataConverter.py")
    sys.exit(-1)


if __name__ == "__main__":

    try:
        config_data = Utils.parse_config(CONFIG_FILE)
        logger = setup_log_system(config_data)
    except Exception as ex:
        assert False, "Error in obtaining config data!"
        sys.exit(-1)

    filename = config_data["CSV_DATA"]["FILENAME"]

    if filename:
        if(filename.endswith(".csv")):
            print("Valid CSV file: " + filename)
        else:
            print("Unsupported conversion of: " + filename)
            usage_help()
    else:
        usage_help()

    if filename is not None:
        csvCon = CSVConverter(config_data)
        csvCon.convert_data()
