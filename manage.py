#!/usr/bin/env python

"""
    Management utility for CMX team Capstone project AI/ML/WebScraping component...
"""

import logging
import sys


def run_scrape_app_cli(args):

    if len(args) != 1:
        logging.error('missing input, usage: ... scrape <output-file-name>')
        sys.exit(1)

    output_file_path = args[0]

    from src.scrape import scrape
    scrape(output_file_path)


def main():
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]\t%(message)s')

    if len(sys.argv) < 2:
        logging.error("Usage: python main.py scrape [output file]")
        sys.exit(1)

    match sys.argv[1]:
        case "scrape":
            run_scrape_app_cli(sys.argv[2:])
        case "help" | "-h" | "--help":
            logging.info("Usage: python main.py scrape [output file]")
        case _:
            logging.error("Unrecognized command")
            logging.error("Usage: python main.py scrape [output file]")


if __name__ == "__main__":
    main()
