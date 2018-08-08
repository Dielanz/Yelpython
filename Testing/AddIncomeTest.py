# Group: yelPython
# Members: Ruslan Askerov (ra7kv), Will Daniel (wkd9th), Zach Lynch (zsl2gf), Le Michael Song (ls2ywj), Dylan Weber (dew2ad)

# Testing the websraper

import unittest
from Append_Pop_Income import *

class TestIncome(unittest.TestCase):

    ## test 1 for average city
    def test_income_1(self):
        print(pop_income_dict['Cuyahoga-Falls-Ohio'])
        self.assertEqual(pop_income_dict['Cuyahoga-Falls-Ohio'],(49210, 27862),'check population income file')


    ## test 2 for small city (fewer "," in population)
    def test_income_2(self):
        print(pop_income_dict['Phoenix-Arizona'])
        self.assertEqual(pop_income_dict['Phoenix-Arizona'],(1615041, 26308),'check population income file')

if __name__ == '__main__':
    unittest.main()
