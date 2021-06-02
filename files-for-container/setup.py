#!/usr/bin/python

print("Starting setup")

import yaml

import setup_utils;

setup_utils.stand_up_postgres()
setup_utils.import_clean_data()

setup_utils.stand_up_redis()

setup_utils.start_apps()

setup_utils.stand_up_nginx()
