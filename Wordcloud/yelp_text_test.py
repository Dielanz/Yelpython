# Group: yelPython
# Members: Ruslan Askerov (ra7kv), Will Daniel (wkd9th), Zach Lynch (zsl2gf), Le Michael Song (ls2ywj), Dylan Weber (dew2ad)

# yelp_text_analysis Testing File
# Python: Final Project
# Yelp Data

import unittest
import pandas as pd
import yelp_text_analysis #This will take a few minutes but you need everything in your environment for these unit tests to run

#Instantiate test class inheriting from unittest.TestCase
class TextTestCase(unittest.TestCase):
    
    #test collectStrings method in yelp_text_analysis file
    def test_collectStrings_returns_appended_text(self):
        
        ser = pd.Series(['abc', 'def', 'ghi'])
        self.assertEqual(collectStrings(ser), 'abcdefghi')
    
    #test that filtering to 5 star reviews is working
    def test_data_top_only_has_5_stars(self):
        
        self.assertEqual(top['stars'].unique(), 5)
    
    #test that filtering to 1 star reviews is working
    def test_data_bot_only_has_1_star(self):
        
        self.assertEqual(bot['stars'].unique(), 1)
    
    #test that filtering to users with > 68 reviews is working
    def test_high_has_users_with_more_than_68_reviews(self):
        
        temp = pd.merge(usr, high, on='user_id', how='inner')
        self.assertEqual(sum(temp['review_count'] > 68), temp.shape[0])
    
    #test that filtering to users with 1 review is working
    def test_low_has_users_with_one_review(self):
        
        temp = pd.merge(usr, low, on='user_id', how='inner')
        self.assertEqual(sum(temp['review_count'] == 1), temp.shape[0])

if __name__ == '__main__':
    unittest.main()