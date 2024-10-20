# Weather-Dashboard-with-OpenWeatherAPI

# Overview

The Weather Trends Application allows users to fetch and display weather data for major cities around the world. Users can search for specific cities, view current weather conditions, and see trends over time. The application is built using Django for the backend and Vue.js for the frontend.

# Features

- **Fetch Weather Data**: Automatically fetches weather data for predefined major cities.
- **Search Functionality**: Users can search for any major city and view its current weather, even if it is not in the predefined list.
- **Dynamic Data Storage**: New city data can be added to the database if the searched city is not already present.
- **User-Friendly Interface**: An aesthetic and responsive design for easy navigation and data visualization.
- **Real-time Updates**: Weather data is refreshed at regular intervals.

# Technologies Used

- **Frontend**: Vue.js, Axios
- **Backend**: Django, Django REST Framework
- **Database**: django-SQLite
- **Environment Management**: Django-environ, python-dotenv

# Installation

Follow the instructions below to set up the project locally.

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python** (version 3.6 or higher)
- **Pip** (Python package installer)
- **Django** (latest version)
- **Docker** (optional, for containerized deployment)
- **Docker Compose** (optional, if using Docker)

### Clone the Repository

1. Open your terminal or command prompt.
2. Clone the repository using the following command:
   -git clone https://github.com/yourusername/your-repository-name.git
   
### Setup_Virtual_Environment
- It’s a good practice to use a virtual environment. Create one using: `python -m venv venv`.
- Activate it using ` source venv\Scripts\activate`

### Install_Dependencies
-With the virtual environment activated, install the required packages: `pip install -r requirements.txt`.

### Configure_Environment_Variables
- Create a `.env` file in `project_dir/env/env_file`. Use it to store API_KEY.
- load it using python-dotenv.

### Run_Migrations
- Run the following command to apply the database migrations:
- `python manage.py makemigrations`
- `python manage.py migrate`

# Running the project
- To start the backend server, navigate to your Django project directory and run the following command: `python manage.py runserver`.
- Navigate to the Frontend Directory. Open another terminal window or tab, and run the following command: `npm run serve`.

# API Endpoints
### Weather Data

- **GET** `/weather/` - Fetches weather data for predefined cities.
- **GET** `/search_city_weather/` - Fetches weather data for a specific city.

### Weather Management

- **GET** `/get_cities/` - Retrieves a list of all available cities in the database.
- **GET** `/get_summary/<str:city>/` - Fetches a summary of weather data for a specific city.
- **GET** `/get_trends/<str:city>/<str:period>/` - Retrieves weather trends for a specific city over a defined time period.
- **POST** `/save_thresholds/` - Saves threshold values for alerts.
- **GET** `/check_alerts/` - Checks and retrieves any active alerts based on the saved thresholds.

# Dependencies

List of dependencies required to run the application can be found in the `requirements.txt` file.

# Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss changes.

# Acknowledgements

Thanks to the developers of Django, Vue.js, and all the libraries and tools that made this project possible.
