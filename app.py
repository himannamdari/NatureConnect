import streamlit as st
import pandas as pd
import sys
import os

# Add the current directory to the Python path
# This helps Python find the utils module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.trail_finder import find_nearby_trails
from utils.event_manager import get_upcoming_events
from utils.biophilia_calculator import calculate_biophilia_score
import config

# Page configuration
st.set_page_config(
    page_title="NatureConnect",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# Sidebar
st.sidebar.title("NatureConnect")
st.sidebar.image("https://i.imgur.com/gJUcYCn.png", width=100)  # Nature icon placeholder

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
        st.session_state.user_location = {"zip": zip_code, "lat": 0, "lon": 0}
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
    st.write("Welcome to NatureConnect, your companion for discovering and connecting with nature.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Nearby Trails")
        if st.session_state.user_location:
            trails = find_nearby_trails(st.session_state.user_location, limit=3)
            for trail in trails:
                st.write(f"**{trail['name']}** - {trail['distance']} miles away")
        else:
            st.info("Set your location to see nearby trails")
    
    with col2:
        st.subheader("Upcoming Nature Events")
        events = get_upcoming_events(limit=3)
        for event in events:
            st.write(f"**{event['name']}** - {event['date']}")
            st.write(event['description'][:100] + "...")
    
    st.subheader("Your Biophilia Score")
    if st.session_state.biophilia_score:
        st.metric("Current Score", f"{st.session_state.biophilia_score}/100")
        st.progress(st.session_state.biophilia_score/100)
    else:
        st.info("Take the quiz to discover your biophilia score")
        if st.button("Take Biophilia Quiz"):
            # Switch to biophilia page
            page = "Biophilia Score"

elif page == "Find Trails":
    st.title("Find Nature Trails Near You")
    
    if not st.session_state.user_location:
        st.warning("Please set your location to find nearby trails")
    else:
        st.write(f"Showing trails near {st.session_state.user_location.get('zip', 'your location')}")
        
        # Trail filters
        col1, col2, col3 = st.columns(3)
        with col1:
            distance = st.slider("Maximum Distance (miles)", 1, 50, 10)
        with col2:
            difficulty = st.multiselect("Difficulty", ["Easy", "Moderate", "Hard"], default=["Easy", "Moderate"])
        with col3:
            features = st.multiselect("Features", ["Waterfall", "Lake", "Mountain View", "Forest", "Wildlife"])
        
        # Find trails with filters
        trails = find_nearby_trails(st.session_state.user_location, distance=distance, 
                                   difficulty=difficulty, features=features)
        
        # Display trails
        if trails:
            for trail in trails:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(trail['name'])
                    st.write(f"**Distance:** {trail['distance']} miles away")
                    st.write(f"**Length:** {trail['length']} miles")
                    st.write(f"**Difficulty:** {trail['difficulty']}")
                    st.write(f"**Features:** {', '.join(trail['features'].split(','))}")
                    st.write(trail['description'])
                with col2:
                    st.image(trail.get('image_url', 'https://i.imgur.com/3Cm5BM9.jpg'), width=200)
                    if st.button("Save to Favorites", key=f"fav_{trail['id']}"):
                        if trail not in st.session_state.favorite_trails:
                            st.session_state.favorite_trails.append(trail)
                            st.success("Added to favorites!")
                st.divider()
        else:
            st.info("No trails found with your selected filters. Try adjusting your criteria.")

elif page == "Nature Events":
    st.title("Discover Nature Events")
    
    # Event filters
    col1, col2 = st.columns(2)
    with col1:
        date_range = st.date_input("Date Range", [pd.Timestamp.now(), pd.Timestamp.now() + pd.Timedelta(days=30)])
    with col2:
        event_types = st.multiselect("Event Types", ["Guided Hike", "Conservation", "Education", "Birdwatching", "Community"])

    # Get events with filters
    events = get_upcoming_events(date_range=date_range, types=event_types)
    
    # Display events
    if events:
        for event in events:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(event['name'])
                st.write(f"**Date:** {event['date']}")
                st.write(f"**Location:** {event['location']}")
                st.write(f"**Type:** {event['type']}")
                st.write(event['description'])
            with col2:
                st.image(event.get('image_url', 'https://i.imgur.com/YJOX1CW.jpg'), width=200)
                if st.button("Register", key=f"reg_{event['id']}"):
                    if event not in st.session_state.registered_events:
                        st.session_state.registered_events.append(event)
                        st.success("Registered!")
            st.divider()
    else:
        st.info("No events found with your selected filters. Try adjusting your criteria.")

elif page == "Biophilia Score":
    st.title("Discover Your Connection to Nature")
    st.write("Answer these questions to calculate your biophilia score - a measure of your connection to the natural world.")
    
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
        st.write(f"**Q{i+1}: {question}**")
        answer = st.slider("", 1, 10, 5, key=f"q{i}")
        answers.append(answer)
        st.write("")
    
    if st.button("Calculate My Score"):
        score = calculate_biophilia_score(answers)
        st.session_state.biophilia_score = score
        
        st.success(f"Your Biophilia Score: {score}/100")
        st.progress(score/100)
        
        if score < 40:
            st.write("Your connection to nature could be stronger. We recommend starting with small steps like visiting a local park weekly.")
        elif score < 70:
            st.write("You have a moderate connection to nature. Try deepening your relationship through regular nature activities.")
        else:
            st.write("You have a strong connection to nature! Consider sharing your passion with others or joining conservation efforts.")
            
        # Recommendations
        st.subheader("Personalized Recommendations")
        recommended_trails = find_nearby_trails(st.session_state.user_location, limit=2) if st.session_state.user_location else []
        recommended_events = get_upcoming_events(limit=2)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Recommended Trails:**")
            for trail in recommended_trails:
                st.write(f"- {trail['name']}")
        with col2:
            st.write("**Recommended Events:**")
            for event in recommended_events:
                st.write(f"- {event['name']} on {event['date']}")

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
                    st.write(f"**{trail['name']}**")
                    st.write(f"Distance: {trail['distance']} miles away | Length: {trail['length']} miles")
                with col2:
                    if st.button("Remove", key=f"remove_{trail['id']}"):
                        st.session_state.favorite_trails.remove(trail)
                        st.experimental_rerun()
                st.divider()
        else:
            st.info("You haven't saved any favorite trails yet.")
    
    with tab2:
        st.subheader("Your Registered Events")
        if st.session_state.registered_events:
            for event in st.session_state.registered_events:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{event['name']}**")
                    st.write(f"Date: {event['date']} | Location: {event['location']}")
                with col2:
                    if st.button("Cancel", key=f"cancel_{event['id']}"):
                        st.session_state.registered_events.remove(event)
                        st.experimental_rerun()
                st.divider()
        else:
            st.info("You haven't registered for any events yet.")
    
    with tab3:
        st.subheader("Nature Journal")
        
        # Add new journal entry
        st.write("**Add New Entry**")
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
            st.write("**Previous Entries**")
            for entry in reversed(st.session_state.nature_journal):
                st.write(f"**{entry['date']} - {entry['location']}**")
                st.write(f"Observations: {entry['observations']}")
                st.write(f"Feelings: {entry['feelings']}")
                if entry['has_photo']:
                    st.write("Photo attached")
                st.divider()
        else:
            st.info("Your nature journal is empty. Start recording your experiences!")

# Footer
st.markdown("---")
st.markdown("NatureConnect © 2025 | Reconnecting people with the natural world")
