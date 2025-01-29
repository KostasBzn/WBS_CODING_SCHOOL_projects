# GANS E-Scooter Airport Data Collector

## Description
This project collects real-time weather and flight data to support GANS, a company planning to deploy e-scooters at airports. The application fetches and processes weather forecasts and flight schedules to optimize e-scooter operations, providing valuable insights for airport logistics and planning.

## Features
- Fetches weather data from multiple cities
- Collects real-time flight data from the airports near these cities
- Provides insights into flight schedules to optimize e-scooter availability

## Technologies Used
- Python
- Requests (for fetching data)
- BeautifulSoup (for web scraping)
- Pandas (for data processing)
- SQLAlchemy (for database integration)
- PyMySQL (for MySQL database connection)
- python-dotenv (for environment variable management)

## Installation
1. Clone the repository:
   git clone git@github.com:KostasBzn/Gans_Scooters_Data_Scraper.git

2. Install the required dependencies:
   pip install -r requirements.txt