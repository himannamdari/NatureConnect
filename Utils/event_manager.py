import pandas as pd
import os
from datetime import datetime, timedelta

def get_upcoming_events(date_range=None, types=None, limit=None):
    """
    Get upcoming nature events with optional filters
    
    Parameters:
    - date_range: tuple of (start_date, end_date)
    - types: list of event types to include
    - limit: maximum number of events to return
    
    Returns:
    - list of event dictionaries
    """
    # In a real app, this would query an API or database
    # For this example, we'll load from a sample CSV file
    
    try:
        # Try to load the sample data
        events_df = pd.read_csv('data/sample_events.csv')
    except FileNotFoundError:
        # If the file doesn't exist, create sample data
        events_df = create_sample_events_data()
    
    # Convert date strings to datetime objects
    events_df['date_obj'] = pd.to_datetime(events_df['date'])
    
    # Apply date range filter
    if date_range is not None and len(date_range) == 2:
        start_date, end_date = date_range
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        events_df = events_df[(events_df['date_obj'] >= start_date) & 
                              (events_df['date_obj'] <= end_date)]
    
    # Apply event type filter
    if types is not None and len(types) > 0:
        events_df = events_df[events_df['type'].isin(types)]
    
    # Sort by date
    events_df = events_df.sort_values('date_obj')
    
    # Limit results
    if limit is not None:
        events_df = events_df.head(limit)
    
    # Remove the date_obj column before returning
    events_df = events_df.drop('date_obj', axis=1)
    
    # Convert to list of dictionaries
    events = events_df.to_dict('records')
    
    return events

def create_sample_events_data():
    """Create sample event data and save to CSV"""
    # Current date for generating events
    now = datetime.now()
    
    events = [
        {
            'id': 1,
            'name': 'Guided Bird Watching Tour',
            'date': (now + timedelta(days=3)).strftime('%Y-%m-%d'),
            'location': 'Oakridge Nature Reserve',
            'type': 'Birdwatching',
            'description': 'Join our expert ornithologists for a guided tour to spot and identify local bird species. Binoculars provided!',
            'image_url': 'https://i.imgur.com/YJOX1CW.jpg'
        },
        {
            'id': 2,
            'name': 'Forest Bathing Experience',
            'date': (now + timedelta(days=5)).strftime('%Y-%m-%d'),
            'location': 'Pinecrest Woods',
            'type': 'Guided Hike',
            'description': 'Experience the Japanese practice of Shinrin-yoku (forest bathing) to reduce stress and boost wellbeing through mindful nature immersion.',
            'image_url': 'https://i.imgur.com/3Cm5BM9.jpg'
        },
        {
            'id': 3,
            'name': 'River Cleanup Volunteer Day',
            'date': (now + timedelta(days=7)).strftime('%Y-%m-%d'),
            'location': 'Silverstream River',
            'type': 'Conservation',
            'description': 'Help restore the natural beauty of our local river by joining our cleanup effort. All equipment provided, plus lunch for volunteers!',
            'image_url': 'https://i.imgur.com/K58U4dV.jpg'
        },
        {
            'id': 4,
            'name': 'Wildflower Identification Workshop',
            'date': (now + timedelta(days=10)).strftime('%Y-%m-%d'),
            'location': 'Meadow View Park',
            'type': 'Education',
            'description': 'Learn to identify local wildflower species and understand their ecological importance in this hands-on workshop.',
            'image_url': 'https://i.imgur.com/VmFbVmE.jpg'
        },
        {
            'id': 5,
            'name': 'Family Nature Scavenger Hunt',
            'date': (now + timedelta(days=12)).strftime('%Y-%m-%d'),
            'location': 'Community Wilderness Area',
            'type': 'Community',
            'description': 'A fun event for families to explore nature together through an educational scavenger hunt with prizes!',
            'image_url': 'https://i.imgur.com/B4mJErA.jpg'
        },
        {
            'id': 6,
            'name': 'Sunset Yoga in the Park',
            'date': (now + timedelta(days=14)).strftime('%Y-%m-%d'),
            'location': 'Hilltop Gardens',
            'type': 'Community',
            'description': 'Connect with nature through outdoor yoga as the sun sets. All skill levels welcome. Bring your own mat.',
            'image_url': 'https://i.imgur.com/QLKL9F5.jpg'
        },
        {
            'id': 7,
            'name': 'Native Plant Gardening Workshop',
            'date': (now + timedelta(days=17)).strftime('%Y-%m-%d'),
            'location': 'Community Center',
            'type': 'Education',
            'description': 'Learn how to create a garden that supports local ecosystems using native plant species. Take home a starter plant!',
            'image_url': 'https://i.imgur.com/Gju4kCM.jpg'
        },
        {
            'id': 8,
            'name': 'Stargazing Night',
            'date': (now + timedelta(days=20)).strftime('%Y-%m-%d'),
            'location': 'Mountain Ridge Observatory',
            'type': 'Education',
            'description': 'Join amateur astronomers to observe stars, planets, and constellations. Telescopes provided. Hot chocolate served!',
            'image_url': 'https://i.imgur.com/bIziVdO.jpg'
        },
        {
            'id': 9,
            'name': 'Nature Photography Workshop',
            'date': (now + timedelta(days=22)).strftime('%Y-%m-%d'),
            'location': 'Wildlife Sanctuary',
            'type': 'Education',
            'description': 'Learn techniques for capturing stunning nature photographs with your smartphone or camera. All skill levels welcome.',
            'image_url': 'https://i.imgur.com/Y2JJ6KQ.jpg'
        },
        {
            'id': 10,
            'name': 'Trail Maintenance Day',
            'date': (now + timedelta(days=25)).strftime('%Y-%m-%d'),
            'location': 'Red Rock Trails',
            'type': 'Conservation',
            'description': 'Help maintain our beloved hiking trails for everyone to enjoy. Tools, training, and refreshments provided.',
            'image_url': 'https://i.imgur.com/Gju4kCM.jpg'
        }
    ]
    
    # Create DataFrame
    events_df = pd.DataFrame(events)
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    events_df.to_csv('data/sample_events.csv', index=False)
    
    return events_df
