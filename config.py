"""
Configuration settings for the NatureConnect application
"""

# App information
APP_NAME = "NatureConnect"
APP_VERSION = "0.1.0"
APP_DESCRIPTION = "Connect with nature around you and boost your biophilia score"

# Default location (San Francisco)
DEFAULT_LOCATION = {
    "lat": 37.7749,
    "lon": -122.4194,
    "city": "San Francisco",
    "state": "CA"
}

# For a real app, you would use a proper API key management system
# These are placeholders and would NOT be stored in code
MAPS_API_KEY = "YOUR_MAPS_API_KEY_HERE"  # For a real app, use env variables
TRAILS_API_KEY = "YOUR_TRAILS_API_KEY_HERE"  # For a real app, use env variables

# Interface settings
PAGE_ICON = "🌿"
THEME_COLOR = "#2E7D32"  # Forest Green
SECONDARY_COLOR = "#81C784"  # Light Green

# Data settings
DATA_FOLDER = "data"
USER_DATA_EXPIRY_DAYS = 30  # How long to keep user data

# Difficulty levels for trails
TRAIL_DIFFICULTY_LEVELS = ["Easy", "Moderate", "Hard"]

# Trail features
TRAIL_FEATURES = [
    "Waterfall",
    "Lake",
    "River",
    "Mountain View",
    "Forest",
    "Wildlife",
    "Wildflowers",
    "Educational",
    "Sunset Views",
    "Historical Site",
    "Accessible"
]

# Event types
EVENT_TYPES = [
    "Guided Hike",
    "Conservation",
    "Education",
    "Birdwatching",
    "Community",
    "Family Friendly",
    "Volunteer",
    "Workshop",
    "Camping"
]
