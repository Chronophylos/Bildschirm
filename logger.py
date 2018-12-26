
def create_logger(name):
    import yaml
    import logging
    import logging.config

    # load logger
    with open("logging.yaml") as logging_yaml:
        logging.config.dictConfig(yaml.load(logging_yaml))

    # create logger
    return logging.getLogger(name)
