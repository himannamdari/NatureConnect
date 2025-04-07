# Data Directory

This directory stores data files for the NatureConnect application.

## Sample Data Files

The following sample data files will be automatically generated when the application runs for the first time:

- `sample_trails.csv` - Sample trail data
- `sample_events.csv` - Sample nature events data

## User Data Files

User data is stored in JSON format:

- `user_[id].json` - Individual user data files

Note: User data files are excluded from Git using the `.gitignore` configuration.

## Data Structure

### Trails Data

Each trail record includes the following fields:
- `id` - Unique identifier
- `name` - Trail name
- `latitude` - Geographic coordinate
- `longitude` - Geographic coordinate
- `length` - Trail length in miles
- `difficulty` - Difficulty level (Easy, Moderate, Hard)
- `features` - Comma-separated list of trail features
- `description` - Text description of the trail
- `image_url` - URL to trail image

### Events Data

Each event record includes the following fields:
- `id` - Unique identifier
- `name` - Event name
- `date` - Event date (YYYY-MM-DD)
- `location` - Event location name
- `type` - Event type/category
- `description` - Text description of the event
- `image_url` - URL to event image

### User Data

Each user record includes:
- `user_id` - Unique identifier
- `created_at` - Account creation timestamp
- `biophilia_score` - Latest biophilia score
- `favorite_trails` - Array of saved trail objects
- `registered_events` - Array of registered event objects
- `nature_journal` - Array of journal entry objects
