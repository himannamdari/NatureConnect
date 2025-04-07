"""
Utility modules for the NatureConnect application.
"""

from utils.trail_finder import find_nearby_trails
from utils.event_manager import get_upcoming_events
from utils.biophilia_calculator import calculate_biophilia_score, get_biophilia_recommendations
from utils.database import SimpleDB

__all__ = [
    'find_nearby_trails',
    'get_upcoming_events',
    'calculate_biophilia_score',
    'get_biophilia_recommendations',
    'SimpleDB'
]
