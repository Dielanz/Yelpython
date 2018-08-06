import unittest
from AddIncomeData_toBusinessCsv import *

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
    
    
    
