import logging
import sys


train_logger = logging.getLogger("TRAIN")
train_logger.setLevel(logging.INFO)
generate_logger = logging.getLogger("GENERATE")
generate_logger.setLevel(logging.INFO)
webparser_logger = logging.getLogger("WEBPARSER")
webparser_logger.setLevel(logging.INFO)
text_gen_logger = logging.getLogger("TEXTGENERATOR")
text_gen_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("logger.log")
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

train_logger.addHandler(file_handler)
generate_logger.addHandler(file_handler)
webparser_logger.addHandler(file_handler)
text_gen_logger.addHandler(file_handler)


def scan_dir(to_wrap):
    def wrapper(path):
        train_logger.info("Scanning directory %s ..." % path)
        try:
            to_wrap(path)
        except (NotADirectoryError, PermissionError, FileNotFoundError):
            train_logger.error("Invalid path or no permission, terminating.")
            print('Cannot find/scan directory.')
            sys.exit(1)

    return wrapper


def scan_stdin(to_wrap):
    def wrapper():
        train_logger.info("Getting data from stdin...")
        to_wrap()
        train_logger.info("Done!")

    return wrapper


def store_model(to_wrap):
    def wrapper(model_path):
        if model_path is None:
            train_logger.error(
                "Path for storing model is not defined, terminating.")
            print('No file to store model.')
            sys.exit(1)
        train_logger.info("Storing model...")
        try:
            to_wrap(model_path)
            train_logger.info("Model stored to %s" % model_path)
        except (PermissionError, NotADirectoryError, FileNotFoundError, 
            IsADirectoryError):
            train_logger.error("Invalid path or no permission, terminating.")
            print("Invalid path or no permission to %s." % model_path)
            sys.exit(1)
        train_logger.info("Training is done!")

    return wrapper


def scan_model(to_wrap):
    def wrapper(model_path):
        if model_path is None:
            generate_logger.error(
                "Path for getting model is not defined, terminating.")
            print('No file to scan model.')
            sys.exit(1)
        generate_logger.info("Loading model...")
        try:
            to_wrap(model_path)
        except (PermissionError, NotADirectoryError, FileNotFoundError, 
            IsADirectoryError):
            generate_logger.error(
                "Invalid path or no permission, terminating.")
            print("Invalid path or no permission to %s." % model_path)
            sys.exit(1)
        generate_logger.info("Done!")

    return wrapper


def generate_sequence(to_wrap):
    def wrapper(output, length, seed):
        generate_logger.info("Generating sequence.")
        to_wrap(output, length, seed)

    return wrapper
