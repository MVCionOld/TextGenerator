import argparse
import os
import sys

import config
import model
import debugging


@debugging.scan_model
def scan_model(model_path):
    """

    Loads stored model.

    :param model_path: path where model ('model.pkl') was stored
    :return: None
    """
    with open(model_path, "rb") as file:
        freq_model.load(file)


@debugging.generate_sequence
def generate_sequence(output, length, seed):
    """
    Generate sequence to the 'output' with 'length', started with 'seed'
    """
    freq_model.generate_text(output, length, seed)


if __name__ == '__main__':

    freq_model = model.Model(config.N_GRAM_SIZE)

    parser = argparse.ArgumentParser()
    for argument, description in config.generate_args.items():
        parser.add_argument(argument, help=description)
    parser_namespace, _ = parser.parse_known_args()

    try:
        parser_namespace.length = int(parser_namespace.length)
    except (ValueError, TypeError):
        print("Cannot parse sequence's length")
        sys.exit(1)

    scan_model(parser_namespace.model)

    generate_sequence(parser_namespace.output,
                      parser_namespace.length, parser_namespace.seed)
