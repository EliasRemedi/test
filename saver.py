# -*- coding: UTF-8 -*-

import csv
import os
from tools import Tools


class Saver:
    """
        This class contains the method needed to save the information into csv file
    """

    def __init__(self, file_name):
        """
            Instantiate an object for the Saver class
        :param file_name: nome of the .csv file
        """
        self.__tools_obj = Tools()
        self.__ConfigDict = self.__tools_obj.ini('config.ini')
        self.__Logger = Tools().get_logger("./")
        self.__FileName = os.path.join(self.__ConfigDict['csv_path'], file_name)

    def save(self, result_dict):
        """
            This method write a new row in a CSV file, and write headers if don't exist.
        :param result_dict: dictionary containing the product information
        """
        try:
            with open("{}.csv".format(self.__FileName), mode='a', encoding='utf-8') as csv_file:
                field_names = result_dict.keys()
                writer = csv.DictWriter(csv_file, fieldnames=field_names, delimiter=';', lineterminator='\n')

                if os.stat("{}.csv".format(self.__FileName)).st_size == 0:
                    writer.writeheader()

                writer.writerow(result_dict)

        except Exception as e:
            text = '::Saver:: Error found trying to Save Data. {}'.format(e)
            self.__Logger.error(text)
