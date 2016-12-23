#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import os
import json
from argparse import ArgumentParser
import svgwrite

class Element():
    def __init__(self, info):
        self.data = info
        self.name = info['NAME']
        self.weight = info['ATOMIC_WEIGHT']
        self.number = info['ATOMIC_NUMBER']
        self.symbol = info['SYMBOL']

    def show(self):
        print('Name: {}'.format(self.name))
        print('Symbol: {}'.format(self.symbol))
        print('Atomic Weight: {}'.format(self.weight))
        print('Atomic Number: {}'.format(self.number))

    def show_detailed(self):
        print(self.data)

    def create_graphic(self):
        file_name = '{}.svg'.format(self.name)
        # Open new vector file
        graphic = svgwrite.Drawing(file_name, profile='tiny')  # 'tiny' or 'full'; what's the difference?


def parse_atoms(json_file):
    with open(json_file, 'r') as table:
        t = json.load(table)
        for atom in t['PERIODIC_TABLE']['ATOM']:
            matter = Element(atom)
            matter.show()

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('json_file', type=str, help='path to json containing element data')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    parse_atoms(args.json_file)

if __name__ == '__main__':
    main()


"""
SAMPLE ELEMENT

            {
                "STATE":"SOLID",
                "NAME":"Carbon",
                "ATOMIC_WEIGHT":"12.011",
                "ATOMIC_NUMBER":"6",
                "OXIDATION_STATES":"+/-4, 2",
                "BOILING_POINT":{
                    "UNIT":"Kelvin",
                    "VALUE":"5100"
                },
                "MELTING_POINT":{
                    "UNIT":"Kelvin",
                    "VALUE":"3825"
                },
                "SYMBOL":"C",
                "DENSITY":{
                    "UNIT":"grams/cubic centimeter",
                    "VALUE":"2.26"
                },
                "ELECTRON_CONFIGURATION":"1s2 2s2 p2",
                "COVALENT_RADIUS":{
                    "UNIT":"Angstroms",
                    "VALUE":"0.77"
                },
                "ELECTRONEGATIVITY":"2.55",
                "ATOMIC_RADIUS":{
                    "UNIT":"Angstroms",
                    "VALUE":"0.91"
                },
                "HEAT_OF_VAPORIZATION":{
                    "UNIT":"kilojoules/mole",
                    "VALUE":"715"
                },
                "ATOMIC_VOLUME":{
                    "UNIT":"cubic centimeters/mole",
                    "VALUE":"5.3"
                },
                "IONIZATION_POTENTIAL":"11.26",
                "SPECIFIC_HEAT_CAPACITY":{
                    "UNIT":"Joules/gram/degree Kelvin",
                    "VALUE":"0.709"
                },
                "THERMAL_CONDUCTIVITY":{
                    "UNIT":"Watts/meter/degree Kelvin",
                    "VALUE":"155"
                }
            }
"""