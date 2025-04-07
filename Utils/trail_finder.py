import pandas as pd
import os
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956  # Radius of earth in miles
    return c * r

def find_nearby_trails(user_location, distance=None, difficulty=None, features=None, limit=None):
    """
    Find trails near the user's location with optional filters
    
    Parameters:
    - user_location: dict with 'lat' and 'lon' keys
    - distance: maximum distance in miles
    - difficulty: list of difficulty levels to include
    - features: list of features to include
    - limit: maximum number of trails to return
    
    Returns:
    - list of trail dictionaries
    """
    # In a real app, this would query an API or database
    # For this example, we'll load from a sample CSV file
    
    try:
        # Try to load the sample data
        trails_df = pd.read_csv('data/sample_trails.csv')
    except FileNotFoundError:
        # If the file doesn't exist, create sample data
        trails_df = create_sample_trails_data()
        
    # Calculate distance from user location
    if user_location and 'lat' in user_location and 'lon' in user_location:
        trails_df['distance'] = trails_df.apply(
            lambda row: haversine(
                user_location['lon'], 
                user_location['lat'],
                row['longitude'], 
                row['latitude']
            ),
            axis=1
        )
    else:
        # Default distances if no user location provided
        trails_df['distance'] = range(1, len(trails_df) + 1)
    
    # Apply filters
    if distance is not None:
        trails_df = trails_df[trails_df['distance'] <= distance]
        
    if difficulty is not None and len(difficulty) > 0:
        trails_df = trails_df[trails_df['difficulty'].isin(difficulty)]
        
    if features is not None and len(features) > 0:
        # For features, we're assuming they're stored as comma-separated values
        for feature in features:
            trails_df = trails_df[trails_df['features'].str.contains(feature, case=False)]
    
    # Sort by distance
    trails_df = trails_df.sort_values('distance')
    
    # Limit results
    if limit is not None:
        trails_df = trails_df.head(limit)
    
    # Convert to list of dictionaries
    trails = trails_df.to_dict('records')
    
    return trails

def create_sample_trails_data():
    """Create sample trail data and save to CSV"""
    trails = [
        {
            'id': 1,
            'name': 'Pine Forest Loop',
            'latitude': 37.7749,
            'longitude': -122.4194,
            'length': 3.2,
            'difficulty': 'Easy',
            'features': 'Forest,Wildlife,Scenic Views',
            'description': 'A beautiful loop through old-growth pine forest with abundant wildlife viewing opportunities.',
            'image_url': 'https://i.imgur.com/3Cm5BM9.jpg'
        },
        {
            'id': 2,
            'name': 'Mountain Vista Trail',
            'latitude': 37.8049,
            'longitude': -122.4094,
            'length': 5.8,
            'difficulty': 'Moderate',
            'features': 'Mountain View,Wildflowers,Forest',
            'description': 'Climb to stunning panoramic views of the surrounding mountains and valleys.',
            'image_url': 'https://i.imgur.com/Gju4kCM.jpg'
        },
        {
            'id': 3,
            'name': 'Crystal Lake Path',
            'latitude': 37.7649,
            'longitude': -122.4294,
            'length': 2.5,
            'difficulty': 'Easy',
            'features': 'Lake,Fishing,Wildlife',
            'description': 'An easy walk around a pristine mountain lake with fishing spots and wildlife viewing areas.',
            'image_url': 'https://i.imgur.com/K58U4dV.jpg'
        },
        {
            'id': 4,
            'name': 'Ridgeline Traverse',
            'latitude': 37.7849,
            'longitude': -122.4394,
            'length': 7.2,
            'difficulty': 'Hard',
            'features': 'Mountain View,Waterfall,Forest',
            'description': 'A challenging hike along a mountain ridge with breathtaking views and a hidden waterfall.',
            'image_url': 'https://i.imgur.com/QLKL9F5.jpg'
        },
        {
            'id': 5,
            'name': 'Waterfall Canyon',
            'latitude': 37.7599,
            'longitude': -122.4494,
            'length': 4.6,
            'difficulty': 'Moderate',
            'features': 'Waterfall,Forest,Wildflowers',
            'description': 'Hike through a lush canyon to a spectacular 60-foot waterfall surrounded by wildflowers.',
            'image_url': 'https://i.imgur.com/Y2JJ6KQ.jpg'
        },
        {
            'id': 6,
            'name': 'Ancient Redwood Trail',
            'latitude': 37.8149,
            'longitude': -122.3994,
            'length': 3.0,
            'difficulty': 'Easy',
            'features': 'Forest,Wildlife,Educational',
            'description': 'Walk among ancient redwood trees, some over 500 years old, with educational placards.',
            'image_url': 'https://i.imgur.com/B4mJErA.jpg'
        },
        {
            'id': 7,
            'name': 'Eagle Peak Trail',
            'latitude': 37.7499,
            'longitude': -122.4594,
            'length': 8.4,
            'difficulty': 'Hard',
            'features': 'Mountain View,Wildlife,Forest',
            'description': 'A challenging climb to Eagle Peak with opportunities to see eagles and other birds of prey.',
            'image_url': 'https://i.imgur.com/bIziVdO.jpg'
        },
        {
            'id': 8,
            'name': 'Meadow Wildflower Walk',
            'latitude': 37.8249,
            'longitude': -122.3894,
            'length': 1.8,
            'difficulty': 'Easy',
            'features': 'Wildflowers,Wildlife,Educational',
            'description': 'A gentle walk through meadows filled with seasonal wildflowers and butterflies.',
            'image_url': 'https://i.imgur.com/VmFbVmE.jpg'
        },
        {
            'id': 9,
            'name': 'River Gorge Path',
            'latitude': 37.7449,
            'longitude': -122.4694,
            'length': 5.2,
            'difficulty': 'Moderate',
            'features': 'River,Wildlife,Forest',
            'description': 'Follow a scenic river through a gorge with swimming holes and fishing spots.',
            'image_url': 'https://i.imgur.com/K58U4dV.jpg'
        },
        {
            'id': 10,
            'name': 'Sunset Ridge Trail',
            'latitude': 37.8349,
            'longitude': -122.3794,
            'length': 4.0,
            'difficulty': 'Moderate',
            'features': 'Mountain View,Sunset Views,Wildflowers',
            'description': 'Perfect for evening hikes with spectacular sunset views from multiple vantage points.',
            'image_url': 'https://i.imgur.com/QLKL9F5.jpg'
        }
    ]
    
    # Create DataFrame
    trails_df = pd.DataFrame(trails)
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    trails_df.to_csv('data/sample_trails.csv', index=False)
    
    return trails_df
