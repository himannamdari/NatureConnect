# NatureConnect



NatureConnect is a Streamlit web application that helps users improve their connection with nature by finding nearby trails, participating in nature events, and tracking their biophilia score.

## Features

- **Nearby Trail Finder**: Discover hiking trails and natural areas near you with filtering by distance, difficulty, and features.
- **Nature Events Calendar**: Find and register for guided hikes, conservation activities, and nature education events.
- **Biophilia Score**: Take a quiz to measure your connection to nature and get personalized recommendations.
- **Nature Journal**: Document your experiences in nature with text entries and photos.
- **User Profile**: Save favorite trails and track registered events.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/natureconnect.git
   cd natureconnect
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   streamlit run app.py
   ```

## Usage

1. Set your location via zip code or geolocation.
2. Navigate through the application using the sidebar menu.
3. Find trails near you and save your favorites.
4. Discover and register for upcoming nature events.
5. Take the biophilia quiz to receive personalized recommendations.
6. Record your nature experiences in the journal.

## Project Structure

```
natureconnect/
├── app.py                   # Main application entry point
├── config.py                # Configuration settings
├── requirements.txt         # Project dependencies
├── utils/                   # Utility modules
│   ├── trail_finder.py      # Trail discovery functionality
│   ├── event_manager.py     # Event listing and registration
│   ├── biophilia_calculator.py # Biophilia scoring and recommendations
│   └── database.py          # Simple JSON-based data storage
├── data/                    # Data storage
│   ├── sample_trails.csv    # Sample trail data
│   └── sample_events.csv    # Sample event data
└── tests/                   # Unit tests
    ├── test_trail_finder.py
    ├── test_event_manager.py
    └── test_biophilia_calculator.py
```

## Deployment

The application can be deployed to Streamlit Cloud:

1. Push your code to GitHub.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud).
3. Connect your GitHub repository.
4. Configure your app settings and deploy.

## Future Enhancements

- Integration with real trail databases and APIs
- User authentication system
- Social features to connect with other nature enthusiasts
- Mobile app version with offline functionality
- Integration with fitness trackers and health apps

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by the growing body of research on biophilia and the health benefits of nature connection
- Trail and event data sources would be cited here in a production application
