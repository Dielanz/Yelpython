# yelp_text_analysis Testing File
# Python: Final Project
# Yelp Data

import unittest
import pandas as pd

class TextTestCase(unittest.TestCase):
    
    def test_collectStrings_returns_appended_text(self):
        
        ser = pd.Series(['abc', 'def', 'ghi'])
        self.assertEqual(collectStrings(ser), 'abcdefghi')
    
    def test_data_top_only_has_5_stars(self):
        
        self.assertEqual(top['stars'].unique(), 5)
    
    def test_data_bot_only_has_1_star(self):
        
        self.assertEqual(bot['stars'].unique(), 1)
    
    def test_high_has_users_with_more_than_68_reviews(self):
        
        temp = pd.merge(usr, high, on='user_id', how='inner')
        self.assertEqual(sum(temp['review_count'] > 68), temp.shape[0])
    
    def test_low_has_users_with_one_review(self):
        
        temp = pd.merge(usr, low, on='user_id', how='inner')
        self.assertEqual(sum(temp['review_count'] == 1), temp.shape[0])

if __name__ == '__main__':
    unittest.main()