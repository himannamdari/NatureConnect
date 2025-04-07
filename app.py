import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
from math import radians, cos, sin, asin, sqrt
import json
import base64

# Function to load and display the logo
def get_logo_base64():
    # Check if logo.svg exists, if not create a directory and save it
    logo_path = "assets/logo.svg"
    os.makedirs(os.path.dirname(logo_path), exist_ok=True)
    
    # Return path to logo
    return logo_path

# Function to load local CSS
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Apply CSS if the file exists, otherwise it will be created later
css_path = "assets/style.css"
if os.path.exists(css_path):
    local_css(css_path)

# Page configuration
st.set_page_config(
    page_title="NatureConnect",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Utility functions moved into app.py for simplicity
# Trail finder functions
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
        }
    ]
    
    # Create DataFrame
    trails_df = pd.DataFrame(trails)
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    trails_df.to_csv('data/sample_trails.csv', index=False)
    
    return trails_df

def find_nearby_trails(user_location, distance=None, difficulty=None, features=None, limit=None):
    """
    Find trails near the user's location with optional filters
    """
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
        # For features, they're stored as comma-separated values
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

# Event manager functions
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
        }
    ]
    
    # Create DataFrame
    events_df = pd.DataFrame(events)
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Save to CSV
    events_df.to_csv('data/sample_events.csv', index=False)
    
    return events_df

def get_upcoming_events(date_range=None, types=None, limit=None):
    """
    Get upcoming nature events with optional filters
    """
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

# Biophilia calculator functions
def calculate_biophilia_score(answers):
    """
    Calculate a biophilia score based on quiz answers
    """
    # Simple calculation - sum of answers normalized to 0-100
    if not answers:
        return 0
    
    # Sum all answers
    total = sum(answers)
    
    # Maximum possible score (10 points per question)
    max_score = len(answers) * 10
    
    # Calculate percentage and round to nearest integer
    score = round((total / max_score) * 100)
    
    return score

# App constants
TRAIL_FEATURES = [
    "Waterfall",
    "Lake",
    "River",
    "Mountain View",
    "Forest",
    "Wildlife",
    "Wildflowers",
    "Educational",
    "Sunset Views"
]

EVENT_TYPES = [
    "Guided Hike",
    "Conservation",
    "Education",
    "Birdwatching",
    "Community",
    "Family Friendly",
    "Workshop"
]

# Initialize session state
if 'user_location' not in st.session_state:
    st.session_state.user_location = None
if 'biophilia_score' not in st.session_state:
    st.session_state.biophilia_score = None
if 'favorite_trails' not in st.session_state:
    st.session_state.favorite_trails = []
if 'registered_events' not in st.session_state:
    st.session_state.registered_events = []
if 'nature_journal' not in st.session_state:
    st.session_state.nature_journal = []

# Create assets directory and save CSS and logo files if they don't exist
os.makedirs('assets', exist_ok=True)

# Create CSS file if it doesn't exist
if not os.path.exists(css_path):
    with open(css_path, 'w') as f:
        f.write("""
/* Main theme colors */
:root {
  --primary: #2E7D32;      /* Forest Green */
  --primary-light: #66BB6A;
  --secondary: #81C784;    /* Light Green */
  --accent: #FFC107;       /* Amber */
  --water: #64B5F6;        /* Blue */
  --text-dark: #263238;
  --text-light: #FFFFFF;
  --background: #F8F9FA;
  --card-bg: #FFFFFF;
}

/* Base styling */
.main {
  background-color: var(--background);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: var(--text-dark);
}

/* Title and header styling */
h1, h2, h3 {
  color: var(--primary);
  font-weight: 600;
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 3px solid var(--primary-light);
  padding-bottom: 0.5rem;
}

h2 {
  font-size: 1.8rem;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
}

h3 {
  font-size: 1.3rem;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
}

/* Sidebar styling */
.css-1lcbmhc.e1fqkh3o0, .css-1v3fvcr.egzxvld1 {
  background-color: var(--primary);
  color: var(--text-light);
}

.sidebar .sidebar-content {
  background-color: var(--primary);
  color: var(--text-light);
}

/* Make sidebar text color white */
.sidebar-content * {
  color: var(--text-light) !important;
}

/* Style radio buttons in sidebar */
.stRadio > div {
  background-color: var(--primary-light);
  border-radius: 5px;
  padding: 10px;
}

.stRadio label {
  background-color: var(--card-bg);
  padding: 8px 15px;
  border-radius: 5px;
  margin: 5px 0;
  transition: all 0.3s;
}

.stRadio label:hover {
  background-color: var(--secondary);
  color: var(--text-light);
}

/* Buttons styling */
.stButton > button {
  background-color: var(--primary);
  color: var(--text-light);
  border: none;
  border-radius: 5px;
  padding: 8px 20px;
  font-weight: 600;
  transition: all 0.3s;
}

.stButton > button:hover {
  background-color: var(--primary-light);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Card styling for sections */
.css-1r6slb0.e1tzin5v2 {
  background-color: var(--card-bg);
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 1.5rem;
  border-left: 5px solid var(--primary);
}

/* Image styling */
img {
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Info boxes styling */
.stInfo {
  background-color: var(--water);
  color: var(--text-light);
  padding: 15px;
  border-radius: 8px;
  margin: 1rem 0;
}

/* Success message styling */
.stSuccess {
  border-radius: 8px;
  font-weight: 600;
}

/* Warning message styling */
.stWarning {
  border-radius: 8px;
  font-weight: 600;
}

/* Progress bar styling */
.stProgress > div > div {
  background-color: var(--primary);
}

/* Slider styling */
.stSlider {
  padding-top: 10px;
  padding-bottom: 10px;
}

/* Footer styling */
footer {
  border-top: 1px solid var(--secondary);
  padding-top: 1rem;
  margin-top: 2rem;
  color: var(--primary);
  font-size: 0.9rem;
}

/* Custom divider */
.divider {
  height: 3px;
  background-color: var(--primary-light);
  margin: 1.5rem 0;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
  gap: 10px;
}

.stTabs [data-baseweb="tab"] {
  background-color: var(--background);
  border-radius: 5px 5px 0 0;
  padding: 10px 20px;
  transition: all 0.3s;
}

.stTabs [aria-selected="true"] {
  background-color: var(--primary);
  color: var(--text-light);
}

/* Input fields styling */
.stTextInput > div > div > input, .stTextArea > div > div > textarea {
  border-radius: 5px;
  border: 2px solid var(--primary-light);
  padding: 10px;
  transition: all 0.3s;
}

.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.2);
}

/* Trail and event cards styling */
.card {
  background-color: var(--card-bg);
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 1.5rem;
  border-left: 5px solid var(--primary);
  transition: transform 0.3s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

/* Logo container */
.logo-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.logo {
  width: 120px;
  height: 120px;
}
""")
    
    # Load the CSS after creating it
    local_css(css_path)


# Create SVG logo file if it doesn't exist
logo_path = "assets/logo.svg"
if not os.path.exists(logo_path):
    with open(logo_path, 'w') as f:
        f.write("""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">
  <!-- Background circle -->
  <circle cx="150" cy="150" r="140" fill="#f8f9fa" stroke="#2E7D32" stroke-width="6"/>
  
  <!-- Mountains -->
  <path d="M50,210 L110,130 L170,210" fill="#4CAF50" stroke="#2E7D32" stroke-width="3"/>
  <path d="M130,210 L190,130 L250,210" fill="#388E3C" stroke="#2E7D32" stroke-width="3"/>
  
  <!-- Sun -->
  <circle cx="225" cy="90" r="25" fill="#FFC107" stroke="#FF9800" stroke-width="3"/>
  
  <!-- Tree -->
  <rect x="75" y="170" width="8" height="40" fill="#795548"/>
  <path d="M55,170 L79,120 L103,170 Z" fill="#66BB6A" stroke="#2E7D32" stroke-width="2"/>
  <path d="M60,150 L79,110 L98,150 Z" fill="#66BB6A" stroke="#2E7D32" stroke-width="2"/>
  
  <!-- Water/River -->
  <path d="M50,210 C80,200 100,220 130,210 C160,200 180,220 210,210 C240,200 260,220 290,210 L290,240 L50,240 Z" fill="#64B5F6" stroke="#1976D2" stroke-width="2"/>
  
  <!-- Person silhouette -->
  <circle cx="170" cy="160" r="10" fill="#795548"/>
  <path d="M170,170 L170,195" stroke="#795548" stroke-width="6" stroke-linecap="round"/>
  <path d="M170,180 L160,195" stroke="#795548" stroke-width="4" stroke-linecap="round"/>
  <path d="M170,180 L180,195" stroke="#795548" stroke-width="4" stroke-linecap="round"/>
  
  <!-- Text (optional, can be removed if you prefer a symbol-only logo) -->
  <text x="150" y="265" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle" fill="#2E7D32">NatureConnect</text>
</svg>""")

# Function to render card styling for trails and events
def card_styling(title, content_html):
    return f"""
    <div class="card">
        <h3>{title}</h3>
        {content_html}
    </div>
    """

# Sidebar with improved styling
st.sidebar.markdown(f"""
    <div class="logo-container">
        <img src="./assets/logo.svg" class="logo" alt="NatureConnect Logo">
    </div>
""", unsafe_allow_html=True)

st.sidebar.title("NatureConnect")

# Navigation
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Find Trails", "Nature Events", "Biophilia Score", "My Profile"]
)

# User location input
st.sidebar.subheader("Your Location")
location_method = st.sidebar.radio("Set your location", ["Enter Zip Code", "Use Current Location"])

if location_method == "Enter Zip Code":
    zip_code = st.sidebar.text_input("Enter your zip code")
    if zip_code and st.sidebar.button("Update Location"):
        # In a real app, we would validate and geocode the zip code
        st.session_state.user_location = {"zip": zip_code, "lat": 37.7749, "lon": -122.4194}
        st.sidebar.success(f"Location updated to {zip_code}")
else:
    if st.sidebar.button("Get Current Location"):
        # In a real app, we would use browser geolocation
        # For now we'll use a placeholder
        st.session_state.user_location = {"zip": "00000", "lat": 37.7749, "lon": -122.4194}
        st.sidebar.success("Location updated")

# Main content based on selected page
if page == "Home":
    st.title("Connect with Nature Around You")
    
    # Hero section with styled background
    st.markdown("""
    <div style="background: linear-gradient(rgba(46, 125, 50, 0.7), rgba(46, 125, 50, 0.9)), url(https://i.imgur.com/Gju4kCM.jpg); 
                background-size: cover; 
                padding: 3rem; 
                border-radius: 10px; 
                color: white; 
                margin-bottom: 2rem;
                text-align: center;">
        <h1 style="color: white;">Welcome to NatureConnect</h1>
        <p style="font-size: 1.2rem;">Your companion for discovering and connecting with nature.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Nearby Trails")
        if st.session_state.user_location:
            trails = find_nearby_trails(st.session_state.user_location, limit=3)
            for trail in trails:
                st.markdown(f"""
                <div class="card">
                    <h4>{trail['name']}</h4>
                    <p><strong>Distance:</strong> {trail['distance']:.1f} miles away</p>
                    <p><strong>Difficulty:</strong> {trail['difficulty']}</p>
                    <img src="{trail.get('image_url', 'https://i.imgur.com/3Cm5BM9.jpg')}" style="width:100%; max-height:120px; object-fit:cover;">
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Set your location to see nearby trails")
    
    with col2:
        st.subheader("Upcoming Nature Events")
        events = get_upcoming_events(limit=3)
        for event in events:
            st.markdown(f"""
            <div class="card">
                <h4>{event['name']}</h4>
                <p><strong>Date:</strong> {event['date']}</p>
                <p><strong>Location:</strong> {event['location']}</p>
                <p>{event['description'][:100]}...</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.subheader("Your Biophilia Score")
    if st.session_state.biophilia_score:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.metric("Current Score", f"{st.session_state.biophilia_score}/100")
        with col2:
            st.progress(st.session_state.biophilia_score/100)
            
        # Message based on score
        if st.session_state.biophilia_score < 40:
            message = "Your connection to nature could be stronger. We recommend starting with small steps like visiting a local park weekly."
        elif st.session_state.biophilia_score < 70:
            message = "You have a moderate connection to nature. Try deepening your relationship through regular nature activities."
        else:
            message = "You have a strong connection to nature! Consider sharing your passion with others or joining conservation efforts."
            
        st.info(message)
    else:
        st.info("Take the quiz to discover your biophilia score")
        if st.button("Take Biophilia Quiz", key="home_quiz_button"):
            # For navigation within a single app
            # In a real app with multiple pages, we'd use st.experimental_set_query_params()
            st.session_state.page = "Biophilia Score"
            st.experimental_rerun()

elif page == "Find Trails":
    st.title("Find Nature Trails Near You")
    
    if not st.session_state.user_location:
        st.warning("Please set your location in the sidebar to find nearby trails")
    else:
        st.write(f"Showing trails near {st.session_state.user_location.get('zip', 'your location')}")
        
        # Trail filters in a visually appealing container
        st.markdown("""
        <div style="background-color: #E8F5E9; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="color: #2E7D32; margin-top: 0;">Trail Filters</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            distance = st.slider("Maximum Distance (miles)", 1, 50, 10)
        with col2:
            difficulty = st.multiselect("Difficulty", ["Easy", "Moderate", "Hard"], default=["Easy", "Moderate"])
        with col3:
            features = st.multiselect("Features", TRAIL_FEATURES)
        
        # Find trails with filters
        trails = find_nearby_trails(st.session_state.user_location, distance=distance, 
                                   difficulty=difficulty, features=features)
        
        # Display trails with enhanced styling
        if trails:
            st.markdown(f"<h3>Found {len(trails)} Trails</h3>", unsafe_allow_html=True)
            
            for trail in trails:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                    <div class="card">
                        <h3>{trail['name']}</h3>
                        <p><strong>Distance:</strong> {trail['distance']:.1f} miles away</p>
                        <p><strong>Length:</strong> {trail['length']} miles</p>
                        <p><strong>Difficulty:</strong> {trail['difficulty']}</p>
                        <p><strong>Features:</strong> {', '.join(trail['features'].split(','))}</p>
                        <p>{trail['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.image(trail.get('image_url', 'https://i.imgur.com/3Cm5BM9.jpg'), width=200)
                    if st.button("Save to Favorites", key=f"fav_{trail['id']}"):
                        if trail not in st.session_state.favorite_trails:
                            st.session_state.favorite_trails.append(trail)
                            st.success("Added to favorites!")
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        else:
            st.info("No trails found with your selected filters. Try adjusting your criteria.")

elif page == "Nature Events":
    st.title("Discover Nature Events")
    
    # Event filters with styled container
    st.markdown("""
    <div style="background-color: #E8F5E9; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #2E7D32; margin-top: 0;">Event Filters</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        date_range = st.date_input("Date Range", [pd.Timestamp.now(), pd.Timestamp.now() + pd.Timedelta(days=30)])
    with col2:
        event_types = st.multiselect("Event Types", EVENT_TYPES)

    # Get events with filters
    events = get_upcoming_events(date_range=date_range, types=event_types)
    
    # Display events with enhanced styling
    if events:
        st.markdown(f"<h3>Found {len(events)} Events</h3>", unsafe_allow_html=True)
        
        for event in events:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div class="card">
                    <h3>{event['name']}</h3>
                    <p><strong>Date:</strong> {event['date']}</p>
                    <p><strong>Location:</strong> {event['location']}</p>
                    <p><strong>Type:</strong> {event['type']}</p>
                    <p>{event['description']}</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.image(event.get('image_url', 'https://i.imgur.com/YJOX1CW.jpg'), width=200)
                if st.button("Register", key=f"reg_{event['id']}"):
                    if event not in st.session_state.registered_events:
                        st.session_state.registered_events.append(event)
                        st.success("Registered!")
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    else:
        st.info("No events found with your selected filters. Try adjusting your criteria.")

elif page == "Biophilia Score":
    st.title("Discover Your Connection to Nature")
    
    # Introduction with styled container
    st.markdown("""
    <div style="background-color: #E8F5E9; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #2E7D32; margin-top: 0;">Biophilia Quiz</h3>
        <p>Answer these questions to calculate your biophilia score - a measure of your connection to the natural world.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Biophilia quiz questions
    questions = [
        "How many hours per week do you spend in natural settings?",
        "Do you have plants in your home?",
        "How often do you notice birds, insects, or other wildlife?",
        "Do you prefer natural materials (wood, stone, etc.) in your living space?",
        "How important is access to nature for your well-being?",
        "Do you engage in outdoor recreational activities?",
        "Do you feel a sense of awe or wonder in natural settings?",
        "Do you take action to protect natural environments?",
        "How connected do you feel to the cycles of nature (seasons, day/night)?",
        "Do you seek out information about nature or environmental topics?"
    ]
    
    answers = []
    for i, question in enumerate(questions):
        st.markdown(f"""
        <div style="background-color: #FFFFFF; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #2E7D32;">
            <p><strong>Q{i+1}:</strong> {question}</p>
        </div>
        """, unsafe_allow_html=True)
        answer = st.slider("1 = Not at all, 10 = Very much", 1, 10, 5, key=f"q{i}")
        answers.append(answer)
    
    if st.button("Calculate My Score", key="calculate_score_button"):
        score = calculate_biophilia_score(answers)
        st.session_state.biophilia_score = score
        
        # Result display with styled container
        st.markdown(f"""
        <div style="background: linear-gradient(to right, rgba(46, 125, 50, 0.7), rgba(102, 187, 106, 0.7)); 
                    padding: 20px; 
                    border-radius: 10px; 
                    color: white; 
                    text-align: center;
                    margin-top: 20px;">
            <h2 style="color: white;">Your Biophilia Score: {score}/100</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.progress(score/100)
        
        # Message based on score
        if score < 40:
            message = "Your connection to nature could be stronger. We recommend starting with small steps like visiting a local park weekly."
            color = "#FFC107"  # Amber for low score
        elif score < 70:
            message = "You have a moderate connection to nature. Try deepening your relationship through regular nature activities."
            color = "#4CAF50"  # Green for medium score
        else:
            message = "You have a strong connection to nature! Consider sharing your passion with others or joining conservation efforts."
            color = "#2E7D32"  # Dark green for high score
        
        st.markdown(f"""
        <div style="background-color: {color}; padding: 15px; border-radius: 10px; color: white; margin-top: 15px;">
            <p>{message}</p>
        </div>
        """, unsafe_allow_html=True)
            
        # Recommendations
        st.subheader("Personalized Recommendations")
        recommended_trails = find_nearby_trails(st.session_state.user_location, limit=2) if st.session_state.user_location else []
        recommended_events = get_upcoming_events(limit=2)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="card">
                <h4>Recommended Trails</h4>
                <ul>
            """, unsafe_allow_html=True)
            
            for trail in recommended_trails:
                st.markdown(f"<li>{trail['name']}</li>", unsafe_allow_html=True)
                
            if not recommended_trails:
                st.markdown("<li>Set your location to see trail recommendations</li>", unsafe_allow_html=True)
                
            st.markdown("</ul></div>", unsafe_allow_html=True)
                
        with col2:
            st.markdown("""
            <div class="card">
                <h4>Recommended Events</h4>
                <ul>
            """, unsafe_allow_html=True)
            
            for event in recommended_events:
                st.markdown(f"<li>{event['name']} on {event['date']}</li>", unsafe_allow_html=True)
                
            st.markdown("</ul></div>", unsafe_allow_html=True)

elif page == "My Profile":
    st.title("My Nature Profile")
    
    # Profile tabs
    tab1, tab2, tab3 = st.tabs(["Favorite Trails", "Registered Events", "Nature Journal"])
    
    with tab1:
        st.subheader("Your Favorite Trails")
        if st.session_state.favorite_trails:
            for trail in st.session_state.favorite_trails:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                    <div class="card">
                        <h4>{trail['name']}</h4>
                        <p>Distance: {trail['distance']:.1f} miles away | Length: {trail['length']} miles</p>
                        <p>Difficulty: {trail['difficulty']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("Remove", key=f"remove_{trail['id']}"):
                        st.session_state.favorite_trails.remove(trail)
                        st.experimental_rerun()
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        else:
            st.info("You haven't saved any favorite trails yet.")
    
    with tab2:
        st.subheader("Your Registered Events")
        if st.session_state.registered_events:
            for event in st.session_state.registered_events:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"""
                    <div class="card">
                        <h4>{event['name']}</h4>
                        <p>Date: {event['date']} | Location: {event['location']}</p>
                        <p>Type: {event['type']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("Cancel", key=f"cancel_{event['id']}"):
                        st.session_state.registered_events.remove(event)
                        st.experimental_rerun()
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        else:
            st.info("You haven't registered for any events yet.")
    
    with tab3:
        st.subheader("Nature Journal")
        
        # Add new journal entry with styled container
        st.markdown("""
        <div style="background-color: #E8F5E9; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="color: #2E7D32; margin-top: 0;">Add New Entry</h3>
        </div>
        """, unsafe_allow_html=True)
        
        date = st.date_input("Date", pd.Timestamp.now())
        location = st.text_input("Location")
        observations = st.text_area("What did you observe?")
        feelings = st.text_area("How did it make you feel?")
        photo = st.file_uploader("Upload a photo (optional)", type=["jpg", "png"])
        
        if st.button("Save Journal Entry"):
            if observations and feelings:
                new_entry = {
                    "date": date.strftime("%Y-%m-%d"),
                    "location": location,
                    "observations": observations,
                    "feelings": feelings,
                    "has_photo": photo is not None
                }
                st.session_state.nature_journal.append(new_entry)
                st.success("Journal entry saved!")
            else:
                st.error("Please fill out the required fields.")
        
        # Display journal entries
        if st.session_state.nature_journal:
            st.markdown("""
            <div style="background-color: #E8F5E9; padding: 20px; border-radius: 10px; margin: 30px 0 20px 0;">
                <h3 style="color: #2E7D32; margin-top: 0;">Previous Entries</h3>
            </div>
            """, unsafe_allow_html=True)
            
            for entry in reversed(st.session_state.nature_journal):
                st.markdown(f"""
                <div class="card">
                    <h4>{entry['date']} - {entry['location']}</h4>
                    <p><strong>Observations:</strong> {entry['observations']}</p>
                    <p><strong>Feelings:</strong> {entry['feelings']}</p>
                    {" <p><em>Photo attached</em></p>" if entry['has_photo'] else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Your nature journal is empty. Start recording your experiences!")

# Footer with improved styling
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<footer>
    <p>NatureConnect © 2025 | Reconnecting people with the natural world</p>
    <p style="font-size: 0.8rem;">Created with 💚 for nature enthusiasts everywhere</p>
</footer>
""", unsafe_allow_html=True)
