import unittest
import sys
import os
import pandas as pd
from datetime import datetime, timedelta

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.event_manager import get_upcoming_events, create_sample_events_data

class TestEventManager(unittest.TestCase):
    
    def setUp(self):
        """Set up test cases"""
        # Ensure sample data exists
        self.sample_data = create_sample_events_data()
        
        # Current date for test cases
        self.now = datetime.now()
        self.start_date = self.now
        self.end_date = self.now + timedelta(days=30)
    
    def test_get_upcoming_events_no_filters(self):
        """Test getting events with no filters"""
        events = get_upcoming_events()
        
        # Should return all events, sorted by date
        self.assertEqual(len(events), len(self.sample_data))
        
        # Verify events have the expected fields
        for event in events:
            self.assertIn('id', event)
            self.assertIn('name', event)
            self.assertIn('date', event)
            self.assertIn('location', event)
            self.assertIn('type', event)
            self.assertIn('description', event)
    
    def test_get_upcoming_events_with_date_range(self):
        """Test getting events with date range filter"""
        # Get events for next week only
        next_week_start = self.now + timedelta(days=7)
        next_week_end = self.now + timedelta(days=14)
        
        events = get_upcoming_events(date_range=[next_week_start, next_week_end])
        
        # All events should be within the date range
        for event in events:
            event_date = pd.to_datetime(event['date'])
            self.assertTrue(next_week_start <= event_date <= next_week_end)
    
    def test_get_upcoming_events_with_type_filter(self):
        """Test getting events with type filter"""
        event_types = ['Conservation']
        events = get_upcoming_events(types=event_types)
        
        # All events should have the specified type
        for event in events:
            self.assertIn(event['type'], event_types)
    
    def test_get_upcoming_events_with_limit(self):
        """Test getting events with result limit"""
        limit = 3
        events = get_upcoming_events(limit=limit)
        
        # Should return exactly the number of events specified by limit
        self.assertEqual(len(events), limit)
    
    def test_get_upcoming_events_with_multiple_filters(self):
        """Test getting events with multiple filters applied"""
        event_types = ['Education', 'Community']
        limit = 2
        
        events = get_upcoming_events(
            date_range=[self.start_date, self.end_date],
            types=event_types,
            limit=limit
        )
        
        # Should respect all filters
        self.assertLessEqual(len(events), limit)
        
        for event in events:
            self.assertIn(event['type'], event_types)
            event_date = pd.to_datetime(event['date'])
            self.assertTrue(self.start_date <= event_date <= self.end_date)

if __name__ == '__main__':
    unittest.main()
