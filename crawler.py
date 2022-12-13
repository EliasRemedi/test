# -*- coding: utf-8 -*-

from tools import Tools
import requests
from lxml import html
import pymysql
from datetime import datetime


class Crawler:
    def __init__(self):
        self.__tools_obj = Tools()
        self.__ConfigDict = self.__tools_obj.ini('config.ini')
        self.__logger = Tools().get_logger("./")

    def crawl(self):
        headers = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
        }
        self.__logger.info(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}-----init crawler-----")
        try:
            # # main url
            response = requests.get('https://www.diariopanorama.com/', headers=headers)
            tree = html.fromstring(response.content)
            weather = tree.xpath("//div[@class='tie01']/text()")[0]
            date_weather = datetime.now().strftime('%d/%m/%Y-%H:%M:%S') + ' temperatura de: ' +weather
            self.__logger.info(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')} la temperatura en diario panorama es {weather}")

            #save in DB
            self.__logger.info(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}-----saving in db-----")
            db = pymysql.connect(host=self.__ConfigDict['db_host'], user=self.__ConfigDict['db_user'], password=self.__ConfigDict['db_password'], port=int(self.__ConfigDict['db_port']))
            cursor = db.cursor()
            cursor.execute(f'INSERT INTO test.test (text) values ("{date_weather}");')
            db.commit()
            db.close()
            self.__logger.info(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}-----saved-----")
            self.__logger.info(f"{datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}-----crawler ended successfully-----")

        except Exception as e:
            self.__logger.error(f"fallo crawler {e}")
