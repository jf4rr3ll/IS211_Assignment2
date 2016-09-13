#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 2 Module"""

import datetime
import logging
import urllib2
import argparse
import csv


def main():
    logging.basicConfig(filename='error.log', level=logging.ERROR)
    parser = argparse.ArgumentParser()
    parser.add_argument('--url')
    args = parser.parse_args()

    def downloadData(url):
        """Defines a function which downloads the contents of the URL and returns it to the caller

        Args:
            url (str): the URL where the data to be downloaded is located

        Returns:
            datafile: the data contained in the url."""

        datafile = urllib2.urlopen(url)
        return datafile

    def processData(datafile):
        """Defines a function which processes the data which was downloaded

        Args:
            datafile: the data contained in the url of the previous function.

        Returns:
            data_dict (dict): a dictionary that maps a person's ID to a typle of the form"""

        data_dict = {}
        data_csv = csv.reader(datafile)

        for i in data_csv:
            k = i[0]

            try:
                i[2] = datetime.datetime.strptime(i[2], '%d/%m/%Y')
                v = tuple(i[1], i[2])

            except ValueError:
                id = i[0]
                logging.error('Error: Request for ID #{0} could not be processed.'.format(id))

            finally:
                data_dict = {k:v for k, v in i}

        return data_dict

    def displayPerson(id, personData):
        """Defines a function which prints the name and birthday of a given user based on their ID

        Args:
            id (int): The ID number of the person whose data is being requested
            personData (dict): The dictionary data containing the name and birthday matching the ID

        Returns:
            name_dob: The name and birthday of the person whose data is requested"""
        name_dob = ""

        try:
            name_dob = 'Person #{0} is {1} with a birthday of {2}'.format(id, personData[id][0], personData[id][1])

        except KeyError:
            print "No user found with that ID."

        return name_dob

    if args.url:
        csvData = downloadData(url)
        personData = processData(csvData)

        while True:
            try:
                id = int(raw_input('Please enter the ID #:'))
            except ValueError:
                print 'Invalid input.'
                continue
            if id <= 0:
                sys.exit()
            elif id > 0:
                displayPerson(id, personData)
            else:
                print 'Invalid input. Try again.'
    else:
        print 'Please use --url parameter'

if __name__ == '__main__':
    main()