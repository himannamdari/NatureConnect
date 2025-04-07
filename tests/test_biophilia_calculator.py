import unittest
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.biophilia_calculator import calculate_biophilia_score, get_biophilia_recommendations

class TestBiophiliaCalculator(unittest.TestCase):
    
    def test_calculate_biophilia_score_empty(self):
        """Test score calculation with empty answers"""
        score = calculate_biophilia_score([])
        self.assertEqual(score, 0)
    
    def test_calculate_biophilia_score_min(self):
        """Test score calculation with minimum answers"""
        # 10 questions, all answered with 1 (minimum)
        score = calculate_biophilia_score([1] * 10)
        self.assertEqual(score, 10)
    
    def test_calculate_biophilia_score_max(self):
        """Test score calculation with maximum answers"""
        # 10 questions, all answered with 10 (maximum)
        score = calculate_biophilia_score([10] * 10)
        self.assertEqual(score, 100)
    
    def test_calculate_biophilia_score_mixed(self):
        """Test score calculation with mixed answers"""
        # 10 questions with mixed answers
        score = calculate_biophilia_score([5, 6, 7, 8, 9, 5, 6, 7, 8, 9])
        self.assertEqual(score, 70)
    
    def test_get_biophilia_recommendations_low(self):
        """Test recommendations for low score"""
        recommendations = get_biophilia_recommendations(30)
        self.assertIn('activities', recommendations)
        self.assertIn('resources', recommendations)
        self.assertIn('daily_practices', recommendations)
        # Verify low score specific recommendation is included
        self.assertIn('Visit a local park for 15 minutes daily', recommendations['activities'])
    
    def test_get_biophilia_recommendations_medium(self):
        """Test recommendations for medium score"""
        recommendations = get_biophilia_recommendations(50)
        # Verify medium score specific recommendation is included
        self.assertIn('Try forest bathing (mindful nature immersion)', recommendations['activities'])
    
    def test_get_biophilia_recommendations_high(self):
        """Test recommendations for high score"""
        recommendations = get_biophilia_recommendations(80)
        # Verify high score specific recommendation is included
        self.assertIn('Participate in citizen science projects', recommendations['activities'])
    
    def test_get_biophilia_recommendations_with_location(self):
        """Test recommendations with location data"""
        location = {'lat': 37.7749, 'lon': -122.4194}
        recommendations = get_biophilia_recommendations(50, location)
        self.assertIn('location_based', recommendations)

if __name__ == '__main__':
    unittest.main()
