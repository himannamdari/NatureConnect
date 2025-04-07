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
