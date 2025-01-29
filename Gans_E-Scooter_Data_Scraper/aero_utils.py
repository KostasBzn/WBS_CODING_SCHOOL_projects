from dotenv import load_dotenv
import os
import pandas as pd
import requests
import uuid
from sqlalchemy import create_engine, text

load_dotenv()
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
aero_api_key = os.getenv('FLIGHTS_API_KEY')
weather_api_key = os.getenv('WEATHER_API_KEY')

connection_uri = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'


def remove_timezone(datetime):
    # "2025-01-22 12:20+02:00" -> "2025-01-22 12:20"
    return datetime.split('+')[0]



def fetch_airports(city_list):
    list_for_df = []
    cities_from_sql = pd.read_sql("city", con=connection_uri)

    for city in city_list:
        fetch_city_coord = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={weather_api_key}")
        city_data = fetch_city_coord.json()
        lat = city_data[0]["lat"]
        lon = city_data[0]["lon"]

        url = f"https://aerodatabox.p.rapidapi.com/airports/search/location/{lat}/{lon}/km/50/16"
        querystring = {"withFlightInfoOnly":"true"}

        headers = {
	    "X-RapidAPI-Key": aero_api_key,
	    "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
        }
        

        response = requests.request("GET", url, headers=headers, params=querystring)

        airport_json = response.json()["items"]
        matching_city = cities_from_sql[cities_from_sql["city_name"].str.lower() == city.lower()]
        for airport in airport_json:
            airport_id = str(uuid.uuid4()) 
            airport_data = {
                "airport_id": airport_id,
                "icao": airport["icao"],
                "iata": airport["iata"],
                "airport_name": airport["name"],
                "lat": airport["location"]["lat"],
                "lon": airport["location"]["lon"],
                "city_id": matching_city["city_id"].values[0] 
            }

            list_for_df.append(airport_data)

    return pd.DataFrame(list_for_df)


def fetch_flights_arriving_tomorrow(city_list):

    airports_df = fetch_airports(city_list)
    airports_from_sql = pd.read_sql("airports", con=connection_uri)
    list_for_df = []
    arrivals_data_list = []  

    

    for i, row in airports_df.iterrows():
        icao = row['icao']
        
        url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{icao}"

        querystring = {
            "offsetMinutes": 1440,  
            "durationMinutes": 720,  
            "withLeg": "true",  
            "direction": "Arrival",  
            "withCancelled": "true",  
            "withCodeshared": "true",  
            "withCargo": "true", 
            "withPrivate": "true",  
            "withLocation": "false" 
        }
    
        headers = {
            "X-RapidAPI-Key": aero_api_key,
            "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
        }


        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            list_for_df.append(response.json())  

        
            arrivals_list = response.json().get("arrivals", []) 

            matching_airport = airports_from_sql[airports_from_sql["icao"].str.lower() == icao.lower()]

            for arrival in arrivals_list:
                flight_id = str(uuid.uuid4()) 
                arrivals_data = {
                    "flight_id": flight_id,
                    "scheduledTime": remove_timezone(arrival["arrival"]["scheduledTime"]["local"]),
                    "flight_number": arrival["number"],
                    "status": arrival["status"],
                    "airline_name": arrival["airline"]["name"],
                    "arrival_airport_icao": icao,
                    "departure_airport_icao": arrival.get("departure", {}).get("airport", {}).get("icao", "N/A"),
                    "airport_id": matching_airport["airport_id"].values[0] 
                    }

                arrivals_data_list.append(arrivals_data) 

    arrivals_df = pd.DataFrame(arrivals_data_list) 
    return arrivals_df

def insert_airports(city_list):
    airports_df = fetch_airports(city_list)
    airports_from_sql = pd.read_sql("airports", con=connection_uri)
    
    new_airports = airports_df[~airports_df["airport_name"].isin(airports_from_sql["airport_name"])]
    
    new_airports.to_sql("airports", 
                        con=connection_uri, 
                        if_exists="append", 
                        index=False)
    
def insert_flights_arriving_tomorrow(city_list):
    flights_arriving = fetch_flights_arriving_tomorrow(city_list)
    engine = create_engine(connection_uri)

    with engine.connect() as conn:
        with conn.begin():
            conn.execute(text("DELETE FROM arrivals_data"))
        
           
            flights_arriving.to_sql("arrivals_data", 
                                    con=conn,  
                                    if_exists="append", 
                                    index=False) 

def get_airports():
    airports_from_sql = pd.read_sql("airports", con=connection_uri)
    result_df = airports_from_sql.drop_duplicates()
    return result_df


def get_flights():
    flights_from_sql = pd.read_sql("arrivals_data", con=connection_uri)
    result_df = flights_from_sql.drop_duplicates()
    return result_df

