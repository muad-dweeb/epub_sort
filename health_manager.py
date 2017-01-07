#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utility_exceptions import UtilityException
import pandas
from os import path


def sqlite3_test():
    import sqlite3
    db_path = path.expanduser('~/muad-dweeb/utilities/data/test.tsv')
    try:
        connection = sqlite3.connect(db_path)
    except Exception as e:
        raise UtilityException('Connection to database failed: {}'.format(e))
    c = connection.cursor()

    print('Creating table')
    c.execute('CREATE TABLE ninja_turtles (name text, colour text, weapon text')

    print('Inserting a row of data')
    c.execute("INSERT INTO ninja_turtles VALUES ('Leonardo', 'blue', 'dual katana')")

    print('Saving (committing) the changes')
    connection.commit()

    # Display the table
    for row in c.execute('SELECT * FROM ninja_turtles ORDER BY name'):
        print(row)

    # Close the connection
    connection.close()

"""
Health Data Management
"""

def main():
    # Loads health data from file(s); tsv, csv, db, uncertain at the moment
    date_file = '/home/sir/Documents/Life/Health/tracker/date.tsv'
    mindfulness_file = '/home/sir/Documents/Life/Health/tracker/mindfulness.tsv'
    date_df = pandas.read_table(date_file)
    mindful_df = pandas.read_table(mindfulness_file)

    # View all data
    full_df = pandas.merge(date_df, mindful_df, on='date')
    print(full_df)

    # Save full dataframe
    full_df.to_csv('/home/sir/Documents/Life/Health/tracker/full.tsv', index=False, header=True, sep='\t')

    # Enables insertion of new daily data

    # Allows backfilling by date

if __name__ == '__main__':
    main()


