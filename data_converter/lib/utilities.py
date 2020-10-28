import configparser


def parse_config(configFile):
    assert configFile, "Missing parameter"

    try:
        parser = configparser.ConfigParser(
            interpolation=configparser.ExtendedInterpolation())

        if not parser.read(configFile):
            raise Exception("OSError", "File not found!")

        config_data = {}

        for section in parser.sections():
            # Create an empty dictionary for each section
            config_data[section] = {}

            # Loop through pieces of the section
            for (key, val) in parser.items(section):
                # Add the KEY : value pair
                if(key == 'columns' or key == 'structure'):
                    print(key)
                config_data[section].update({key.upper(): val})

    except KeyError as err:
        err_msg = "{}:{} - Item {} not found in configuration file "\
                  "\"{}\".\n".format(__name__,
                                     "parse_config()",
                                     err.args[0],
                                     configFile)
        raise Exception(err_msg)

    except Exception as xcp:
        err_msg = "{}:{} - Error {} using configuration file name "\
                  "\"{}\".\n".format(__name__,
                                     "parse_config()",
                                     xcp.args[0],
                                     configFile)
        raise Exception(err_msg)

    return config_data
