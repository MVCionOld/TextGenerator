import argparse
import os
import sys

import config
import model
import webparser
import debugging


@debugging.scan_dir
def scan_dir(path):
    for entry in os.scandir(path):
        if not entry.is_file():
            continue
        with open(entry.path, "r") as file:
            debugging.train_logger.info("\tparsing %s..." % entry.name)
            for line in file:
                train(line)


@debugging.scan_stdin
def scan_stdin():
    for line in sys.stdin:
        train(line)


def parse_site(url):
    stream = webparser.WebParser(url).parser_content_stream()
    for line in stream:
        train(line)


def train(line):
    if parser_namespace.lc is not None:
        line = line.lower()
    freq_model.train(line)


@debugging.store_model
def store_model(model_path):
    """

    Stores model.

    :param model_path: path where model (as 'model.pkl') will be stored
    :return: None
    """
    with open(model_path, "wb") as file:
        freq_model.store(file)


if __name__ == '__main__':

    freq_model = model.Model(config.N_GRAM_SIZE)

    parser = argparse.ArgumentParser()
    for argument, description in config.train_args.items():
        parser.add_argument(argument, help=description)
    parser_namespace, _ = parser.parse_known_args()

    if parser_namespace.model is None:
        print('Model is undefined, terminating...')
        sys.exit(1)

    trained = False
    if parser_namespace.input_dir is not None:
        scan_dir(parser_namespace.input_dir)
        trained = True
    if parser_namespace.webparse is not None:
        parse_site(parser_namespace.webparse)
        trained = True
    if not trained:
        scan_stdin()  # accord to the --help

    store_model(parser_namespace.model)
