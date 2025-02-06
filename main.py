#!/usr/bin/env python

import sys


def run_predict_app_cli():
    # TODO call ur function here
    # from src.predict.filename import function_name
    # function_name()
    pass


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


if len(sys.argv) < 2:
    print("Usage: python main.py <predict|scrape|train>")

match sys.argv[1]:
    case "predict":
        run_predict_app_cli()
    case "scrape":
        run_scrape_app_cli()
    case "train":
        run_train_app_cli()
    case _:
        print("Unrecognized command")
        print("Usage: python main.py <predict|scrape|train>")
