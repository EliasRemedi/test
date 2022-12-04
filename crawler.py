# -*- coding: utf-8 -*-

import re
from tools import Tools
import requests
import scraper
import saver
from datetime import datetime


class Crawler:
    def __init__(self):
        self.__proxy_socket = None
        self.__tools_obj = Tools()
        self.__ConfigDict = self.__tools_obj.ini('config.ini')
        self.__logger = Tools().get_logger("./")
        self.__scraper = scraper.Scraper()
        self.__saver = saver.Saver(self.__ConfigDict['filename'])

    def crawl(self):
        """
            This method uses requests to find the url o each product, call the method to extract the information and then
            saves it.
        """
        self.save_db()

        headers = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
        self.__logger.info(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}-----init crawler inna-mageplaza-----")
        try:
            # # main url
            # url = self.__ConfigDict['url']
            # response = requests.get(url, headers=headers)
            # html_text = response.text
            # # find the products urls
            # products_href = re.findall(self.__ConfigDict['products'], html_text)
            # if products_href:
            #     self.__logger.info(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}-----scraping products-----")
            #     for prod_href in products_href:
            #         url = prod_href
            #         response = requests.get(url, headers=headers)
            #         prod_html = response.text
            #         # call the create_dic method to extract the product information
            #         result_dict = self.__scraper.create_dic(prod_html, url)
            #         if result_dict:
            #             # if with get the product information, saves it.
            #             self.__saver.save(result_dict)
            #             print("saved")
            self.__logger.info(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}-----crawler ended successfully-----")

        except Exception as e:
            self.__logger.error(f"fallo crawler {e}")

    def save_db(self):
        
        import pymysql
        self.__logger.info(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}-----saving in db-----")
        db = pymysql.connect(host = 'as-db.clfheeawc0hd.us-east-2.rds.amazonaws.com',user = 'admin',password = 'AutoScraping2019',port = 3306)
        cursor = db.cursor()
        cursor.execute(f'INSERT INTO test.test (text) values ("{datetime.now()} amazon");')
        db.commit()
        db.close()
        self.__logger.info(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}-----saved-----")
