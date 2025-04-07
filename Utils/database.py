import json
import os
from datetime import datetime

class SimpleDB:
    """
    A simple JSON-based database for storing user data
    For a real app, you would use a proper database like SQLite, PostgreSQL, etc.
    """
    def __init__(self, data_folder='data'):
        self.data_folder = data_folder
        # Create data folder if it doesn't exist
        os.makedirs(data_folder, exist_ok=True)
    
    def save_user_data(self, user_id, data):
        """Save user data to a JSON file"""
        file_path = os.path.join(self.data_folder, f"user_{user_id}.json")
        
        # Add timestamp
        data['last_updated'] = datetime.now().isoformat()
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_user_data(self, user_id):
        """Load user data from a JSON file"""
        file_path = os.path.join(self.data_folder, f"user_{user_id}.json")
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return empty data if user file doesn't exist
            return {
                'user_id': user_id,
                'created_at': datetime.now().isoformat(),
                'biophilia_score': None,
                'favorite_trails': [],
                'registered_events': [],
                'nature_journal': []
            }
    
    def update_user_field(self, user_id, field, value):
        """Update a specific field in user data"""
        data = self.load_user_data(user_id)
        data[field] = value
        self.save_user_data(user_id, data)
    
    def add_to_user_array(self, user_id, array_field, item):
        """Add an item to an array field in user data"""
        data = self.load_user_data(user_id)
        
        if array_field not in data:
            data[array_field] = []
        
        # Check if item already exists in array (by id if available)
        if isinstance(item, dict) and 'id' in item:
            # Remove existing item with same id if found
            data[array_field] = [
                existing_item for existing_item in data[array_field] 
                if not (isinstance(existing_item, dict) and 
                        'id' in existing_item and 
                        existing_item['id'] == item['id'])
            ]
        
        # Add the new item
        data[array_field].append(item)
        
        # Save updated data
        self.save_user_data(user_id, data)
    
    def remove_from_user_array(self, user_id, array_field, item_id):
        """Remove an item from an array field in user data by its id"""
        data = self.load_user_data(user_id)
        
        if array_field in data:
            # Filter out the item with matching id
            data[array_field] = [
                item for item in data[array_field] 
                if not (isinstance(item, dict) and 
                        'id' in item and 
                        item['id'] == item_id)
            ]
            
            # Save updated data
            self.save_user_data(user_id, data)
