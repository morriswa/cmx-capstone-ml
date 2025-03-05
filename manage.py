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
    pass
    # input_str = args[0]
    # logging.debug(f'predict app received input |{input_str}|')
    # from src.cmx_capstone_ml_morriswa.predict import predict
    # output_str = predict(input_str)
    # logging.debug(f'predict app received output |{output_str}|')


def run_scrape_app_cli(args):

    if len(args) != 1:
        logging.error('missing input, usage: ... scrape <output-file-name>')
        sys.exit(1)

    output_file_path = args[0]

    from src.cmx_capstone_ml_morriswa.scrape import scrape
    scrape(output_file_path)


def main():
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]\t%(message)s')

    if len(sys.argv) < 2:
        logging.error("Usage: python main.py <predict|scrape>")
        sys.exit(1)

    match sys.argv[1]:
        case "predict":
            run_predict_app_cli(sys.argv[2:])
        case "scrape":
            run_scrape_app_cli(sys.argv[2:])
        case "help" | "-h" | "--help":
            logging.info("Usage: python main.py <predict|scrape|train>")
        case _:
            logging.error("Unrecognized command")
            logging.error("Usage: python main.py <predict|scrape|train>")


if __name__ == "__main__":
    main()
