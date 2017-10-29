#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os
import csv
import re
# import urllib.request
# import requests
from bs4 import BeautifulSoup
from random import uniform
from time import sleep
# from selenium import webdriver

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from libs_scraping.scraper import Scraper


BASE_URL = 'http://www.sceoxyz.com/ispo/en_czhshxx.asp'
DOMEN = 'http://www.sceoxyz.com/ispo/'
FILE = 'sceoxyz.csv'


class Scrap(Scraper):
    def get_link_pages(self, url):
        print('Getting links ...')
        if url is not None:
            if self.is_connected():
                links_all = []
                soup = self.soup(url)
                links = soup.find_all('a')

                for link in links:
                    try:
                        if link['target'] == 'companyinfo':
                            links_all.append(link)
                    except:
                        continue

                links_all = [DOMEN + link['href'] for link in links_all]
                return links_all
        else:
            print('WARNING ! url == None')

    def scraper(self, html):
        if self.is_connected():
            booth = name = brand = address = phone = fax = email = website = profile = categories = None

            soup = BeautifulSoup(html, self.lib_bs)
            # soup = self.soup(url)

            table5 = soup.find(id='Table5')

            try:
                booth = table5.find_all('td', class_='td')[0].text.strip()
            except:
                pass

            try:
                name = table5.find_all('td', class_='td')[1].text.strip()
            except:
                pass

            table6 = soup.find(id='Table6')
            td_gray_list = table6.find_all('td', class_='td-gray')

            for td in td_gray_list:
                if td.text.strip() == 'Brand':
                    try:
                        brand = td.find_next_sibling('td', class_='td').get_text(', ').strip()
                    except:
                        pass

                elif td.text.strip() == 'Address':
                    try:
                        address = td.find_next_sibling('td', class_='td').get_text(', ').strip()
                    except:
                        pass

                elif td.text.strip() == 'Tel':
                    try:
                        phone = td.find_next_sibling('td', class_='td').get_text(', ').strip()
                    except:
                        pass

                elif td.text.strip() == 'Fax':
                    try:
                        fax = td.find_next_sibling('td', class_='td').get_text(', ').strip()
                    except:
                        pass

                elif td.text.strip() == 'Email':
                    try:
                        email = td.find_next_sibling('td', class_='td').get_text(', ').strip()
                    except:
                        pass

                elif td.text.strip() == 'Website':
                    try:
                        website = td.find_next_sibling('td', class_='td').get_text(', ').strip()
                    except:
                        pass

                elif td.text.strip() == 'Company profile / product description':
                    try:
                        profile = td.find_next_sibling('td', class_='td').get_text(', ').strip()
                    except:
                        pass

                elif td.text.strip() == 'Product category':
                    try:
                        categories = td.find_next_sibling('td', class_='td')
                        categories = [cat.text.strip() for cat in categories.find_all('td', width='*')]
                    except:
                        pass

            rez = {
                'booth': booth,
                'name': name,
                'brand': brand,
                'address': address,
                'phone': phone,
                'fax': fax,
                'email': email,
                'website': website,
                'profile': profile,
                'categories': categories,
            }

            return rez

    def save(self, prop, path):
        with open(path, 'w') as csvfile:
            writer = csv.writer(csvfile)
            row_field = (
                'Booth', 'Name', 'Brand', 'Address',
                'Phone', 'Fax', 'Email', 'Website',
                'Profile'
            )

            max_cat = 71
            row_cat = []
            for c in range(1, max_cat):
                row_cat.extend(['Category {}'.format(c)])
            row_cat = tuple(row_cat)

            row_field = row_field + row_cat
            writer.writerow(row_field)

            for el in prop:
                row = (
                    (el['booth']),
                    (el['name']),
                    (el['brand']),
                    (el['address']),
                    (el['phone']),
                    (el['fax']),
                    (el['email']),
                    (el['website']),
                    (el['profile']),
                )

                if el['categories']:
                    for i in range(0, len(el['categories'])):
                        row = row + (el['categories'][i],)

                writer.writerow(row)


    def run(self):
        rez = []
        print('Start ...')
        links = self.get_link_pages(self.url)
        print('Items: ', len(links))

        for link in links:
            print('Scraping: ', link)
            html = self.get_html(link)
            rez.append(self.scraper(html))

        # html = self.get_html('http://www.sceoxyz.com/ispo/eN_ExhibitorInfo.asp?v_ident=900203')
        # rez=[self.scraper(html)]
        self.save(rez, FILE)
        print('All data is saved to the %s.' % FILE)
        print('Finish.')


if __name__ == '__main__':
    scraper = Scrap(BASE_URL)
    scraper.run()
