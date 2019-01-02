#!/usr/bin/env python
# -*- coding: utf-8 -*-

# REFERENCE
# http://hamidadelyar.com/project/auto-trader-scraper/
import random
from os import path
import argparse
from string import punctuation
from bs4 import BeautifulSoup
import requests
from json import loads

import time

from utility_exceptions import UtilityException


def config_json_loader(configuration_file):
    """
    Loads a configuration JSON.
    :param configuration_file: The config file path
    :return: monitors to process and all details associated with them
    """
    json_str = None
    source = path.realpath(__file__)
    config_path = path.join(source.rsplit('/')[0], configuration_file)
    try:
        with open(config_path, 'r') as cf:
            json_str = cf.read()
            config_json = loads(json_str)
    except ValueError as e1:
        raise UtilityException("Invalid json str found:\n{}\n{}".format(json_str, str(e1)))
    except IOError as e2:
        raise UtilityException("Could not read tenant configuration file: {}\n{}".format(configuration_file, str(e2)))
    return config_json


def config_settings_parser(settings):
    """
    Generates monitor configuration settings from a subjson
    :param settings: Settings loaded from a  configuration json
    :return: Monitor's configuration settings (generator)
    """
    try:
        price_min = settings['price']['min']
        price_max = settings['price']['max']
        years_min = settings['years']['min']
        years_max = settings['years']['max']
        makes = settings['makes']
        search_radius = settings['search_radius']
        search_center = settings['search_center']
        styles = settings['styles']
        mpg = settings['mpg']
        max_miles = settings['max_mileage']
    except KeyError as e:
        raise UtilityException("Could not parse settings from configuration: \n\t{}\n{}".format(settings, e))
    return price_min, price_max, years_min, years_max, makes, search_center, search_radius, styles, mpg, max_miles


def url_constructor(search_parameters, first_record=0):
    price_min, price_max, years_min, years_max, makes, search_center, search_radius, styles, mpg, max_miles = search_parameters
    domain = 'http://www.autotrader.com/cars-for-sale/'  # 0
    search_center = search_center.split()
    geo = '{}+{}-{}?'.format(search_center[0], search_center[1], search_center[2])  # 1
    geo_radius = 'searchRadius={}'.format(search_radius)  # 2
    start_year = 'startYear={}'.format(years_min)  # 3
    end_year = 'endYear={}'.format(years_max)  # 4
    max_mileage = 'maxMileage={}'.format(max_miles)  # 5
    style_codes = 'vehicleStyleCodes='
    for i in range(len(styles) - 1):
        style_codes += (styles[i].upper() + ',')
    style_codes += styles[-1].upper()  # 6
    mpg_ranges = 'mpgRanges='
    for i in range(len(mpg) - 1):
        mpg_ranges += '{}MPG,'.format(mpg[i])
    mpg_ranges += '{}MPG'.format(mpg[-1])  # 7
    makes_string = 'mmt=['
    for make in makes:
        makes_string += '{}[][]'.format(make)
    makes_string += ']'  # 8
    min_price = 'minPrice={}'.format(price_min)  # 9
    max_price = 'maxPrice={}'.format(price_max)  # 10
    url = '{0}{1}{2}&{3}&{4}&{5}&{6}&{7}&{8}&{9}&{10}&firstRecord={11}&Log=0'.format(
        domain, geo, geo_radius, start_year, end_year, max_mileage,
        style_codes, mpg_ranges, makes_string, min_price, max_price, first_record)
    return url


def scrape(search_parameters, num_pages):
    # user agent to be spoofed. Need to switch this every now and then.
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.5.2171.95 Safari/537.36"
    # user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    int_page = 0

    # run the scraping until specified page number
    while int_page <= num_pages:
        first_record = int_page * 25
        # url with search results
        url = url_constructor(search_parameters, first_record)
        print(url)

        # have random waits in between requests so as not to get caught whilst web scraping
        time.sleep(random.randint(1, 3))

        r = requests.get(url, data=None, headers={'User-Agent': user_agent})
        soup = BeautifulSoup(r.content, "html.parser")

        # get the adverts
        listings = soup.find('div', {'class': 'listing-results'})
        listings = listings.find_all('div', {'class': 'listing-isClickable'})

        for listing in listings:
            # print(listing)
            try:
                header = listing.find('span', {'class': 'atcui-truncate ymm'})
                header = header.find('span')
                print(header.text)
                listing_url = listing.find('span', {'class': 'atcui-trigger'}).find('h2').find('a').get('href')
                print(listing_url)
                price = listing.find('h4', {'class': 'primary-price'}).find('span').text
                print(price)
                price = int(strip_punctuation(price))
            except AttributeError as e:
                raise UtilityException(e)
        int_page += 1


def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)


def main():
    parser = argparse.ArgumentParser(description='Find a car')
    parser.add_argument('config', type=str, help='filepath to search parameter config file')
    parser.add_argument('num_pages', type=int, help='number of pages to scrape')
    args = parser.parse_args()
    configuration = args.config
    num_pages = args.num_pages
    search_parameters = config_settings_parser(config_json_loader(configuration))
    print(scrape(search_parameters, num_pages))


if __name__ == '__main__':
    main()
