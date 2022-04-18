# -*- coding: UTF-8 -*-

import configparser
import os
import logging


class Tools:
    def __init__(self):
        """
            Instantiate an object for the Tools class
        """
        pass

    @staticmethod
    def get_logger(log_path):
        """
            Create a Logging object
        """
        try:
            logger = logging.getLogger(str(log_path).split("/")[-1])
            if not logger.hasHandlers():
                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

                file_handler = logging.FileHandler(os.path.join(log_path, 'output.log'), mode='a+')
                file_handler.setFormatter(formatter)

                stream_handler = logging.StreamHandler()
                stream_handler.setFormatter(formatter)

                logger.setLevel(logging.INFO)
                logger.addHandler(file_handler)
                logger.addHandler(stream_handler)

            return logger
        except Exception as ve:
            print(ve)
            raise

    @staticmethod
    def ini(file_name_path):
        """
            This method loads a list of variables found in the config.ini file into a dictionary.
        :param file_name_path: path of the config.ini
        :return: config_dict: dictionary with config.ini data
        """

        config_dict = {}
        try:

            config = configparser.RawConfigParser()
            config.read(file_name_path, encoding="utf-8")
            for section in config.sections():
                for var in config[section]:
                    config_dict[var] = config[section][var]
            return config_dict
        except Exception as e:
            text = ("Error found in ini function, ERROR:%s " % e)
            print(text)
            raise
