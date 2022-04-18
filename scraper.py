# -*- coding: utf-8 -*-

import re
from tools import Tools


class Scraper:

    def __init__(self):
        """
        Instantiate an object for the Scraper class
        """
        self.__Logger = Tools().get_logger("./")
        self.__tools_obj = Tools()      # Instance of Tools class
        self.__ConfigDict = self.__tools_obj.ini('config.ini')

    def create_dic(self, prod_html, href):
        """
            This method extract the product information from the product html by regex.
        :return: result_dict: dictionary with the product information
        """
        result_dict = {"name": None,
                       "url": href,
                       "price_name1": None,
                       "price1": None,
                       "price_name2": None,
                       "price2": None,
                       "price_name3": None,
                       "price3": None
                       }
        try:
            try:
                # Get product name
                name = re.search(self.__ConfigDict['name'], href).group(1)
                name = name.replace("magento-2-", "")
                name = name.replace("-extension", "")
                result_dict['name'] = name
            except Exception as e:
                text = '::MainCrawler:: Exception in name scrape section; {}'.format(e)
                self.__Logger.error(text)
                pass

            try:
                # Get price name with regex
                price_name = re.findall(self.__ConfigDict['price_name'], prod_html)
                if price_name:
                    for count, p_name in enumerate(price_name):
                        result_dict[f'price_name{count+1}'] = p_name.upper()
                else:
                    price_name2 = re.findall(self.__ConfigDict['price_name2'], prod_html)
                    if price_name2:
                        for count, p_name2 in enumerate(price_name2):
                            result_dict[f'price_name{count + 1}'] = p_name2.upper()
                    else:
                        price_name3 = re.findall(self.__ConfigDict['price_name3'], prod_html)
                        if price_name3:
                            for count, p_name3 in enumerate(price_name3):
                                p_name3 = re.search(r"(\w+)", p_name3).group(0)
                                result_dict[f'price_name{count + 1}'] = p_name3.upper()
            except Exception as e:
                text = '::MainCrawler:: Exception in price_name scrape section; {}'.format(e)
                self.__Logger.error(text)
                pass

            try:
                # Get price with regex
                prices = re.findall(self.__ConfigDict['price'], prod_html)
                if prices:
                    for count, price in enumerate(prices):
                        value = ''.join(price)
                        result_dict[f'price{count+1}'] = value
                else:
                    prices2 = re.findall(self.__ConfigDict['price2'], prod_html)
                    if prices2:
                        for count, price2 in enumerate(prices2):
                            if "$" not in price2:
                                price2 = "$" + price2
                            result_dict[f'price{count + 1}'] = price2
                    else:
                        prices3 = re.findall(self.__ConfigDict['price3'], prod_html)
                        if prices3:
                            for count, price3 in enumerate(prices3):
                                if price3 == "FREE":
                                    price3 = "0"
                                if "$" not in price3:
                                    price3 = "$" + price3
                                result_dict[f'price{count + 1}'] = price3
                        else:
                            prices4 = re.findall(self.__ConfigDict['price4'], prod_html)
                            if prices4:
                                for count, price4 in enumerate(prices4):
                                    if "$" not in price4:
                                        price4 = "$" + price4
                                    result_dict[f'price{count + 1}'] = price4
                            else:
                                price5 = re.findall(self.__ConfigDict['price5'], prod_html)
                                if price5:
                                    result_dict['price_name1'] = "No name"
                                    result_dict['price1'] = price5[0].replace(" ", "")
                                else:
                                    special = re.findall(self.__ConfigDict['special'], prod_html)
                                    if special:
                                        result_dict['price_name1'] = "No name"
                                        result_dict['price1'] = "FREE"

            except Exception as e:
                text = '::MainCrawler:: Exception in price3 scrape section; {}'.format(e)
                self.__Logger.error(text)
                pass

        except ValueError as ve:
            self.__Logger.error(ve)

        finally:
            # Check if we found at least 1 price_name and price of a product.
            if result_dict['price_name1'] is None and result_dict['price1'] is None:
                return False
            else:
                return result_dict
