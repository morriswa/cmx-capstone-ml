#!/usr/bin/env python

"""
    Management utility for CMX team Capstone project AI/ML/WebScraping component...
"""

import logging
import sys


def run_predict_app_cli(args):

    if len(args) != 1:
        logging.error('missing input, usage: ... predict <input>')
        sys.exit(1)

    input_str = args[0]
    logging.debug(f'predict app received input |{input_str}|')
    from src.cmx_capstone_ml_morriswa.predict import predict
    output_str = predict(input_str)
    logging.debug(f'predict app received output |{output_str}|')


def run_scrape_app_cli():
    # TODO call ur function here
    # from src.scrape.filename import function_name
    # function_name()
    pass


def run_train_app_cli():
    # TODO call ur function here
    # from src.train.filename import function_name
    # function_name()
    pass


def main():
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]\t%(message)s')

    if len(sys.argv) < 2:
        logging.error("Usage: python main.py <predict|scrape|train>")
        sys.exit(1)

    match sys.argv[1]:
        case "predict":
            run_predict_app_cli(sys.argv[2:])
        case "scrape":
            run_scrape_app_cli()
        case "train":
            run_train_app_cli()
        case "help" | "-h" | "--help":
            logging.info("Usage: python main.py <predict|scrape|train>")
        case _:
            logging.error("Unrecognized command")
            logging.error("Usage: python main.py <predict|scrape|train>")


if __name__ == "__main__":
    main()
