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
api_key = os.getenv('WEATHER_API_KEY')

connection_uri = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

def fetch_5_day_forecast (city_name):
    fetch_city_coord = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={api_key}")
    city_data = fetch_city_coord.json()
    lat = city_data[0]["lat"]
    lon = city_data[0]["lon"]
    fetch_weather = requests.get(f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}")
    weather_json = fetch_weather.json()
    return weather_json


def create_static_df (weather_json, city):
    static_data = {
        "city_id": weather_json["city"]["id"], 
        "city_name": city,
        "lat": weather_json["city"]['coord']['lat'],
        "lon": weather_json["city"]['coord']['lon'],
        "country": weather_json["city"]['country']
    }


    df_static_data = pd.DataFrame([static_data])
    return df_static_data


def create_dynamic_df(weather_json, city_id):
    requests_data = []
    for timestamp in weather_json["list"]:
        timestamp_id = str(uuid.uuid4()) 
        timestamp_data = {
        "data_id": timestamp_id, 
        "population": weather_json["city"]["population"],
        "timestamp": timestamp["dt_txt"],
        "temperature": timestamp["main"]["temp"],
        "feels_like": timestamp["main"]["feels_like"],
        "humidity": timestamp["main"]["humidity"],
        "wind_speed": timestamp["wind"]["speed"],
        "sky": timestamp["weather"][0]["description"],
        "sunrise": weather_json["city"]["sunrise"],
        "sunset": weather_json["city"]["sunset"],
        "city_id": city_id
        }
        requests_data.append(timestamp_data)
        
    df_weather_data = pd.DataFrame(requests_data)
    return df_weather_data

def insert_df(city_name):
    weather_json = fetch_5_day_forecast(city_name)
    cities_from_sql = pd.read_sql("SELECT * FROM city", con=connection_uri)

    # Check if city exists in the database
    if city_name in cities_from_sql["city_name"].values:
        city_id = cities_from_sql[cities_from_sql["city_name"] == city_name].iloc[0]["city_id"]
        dynamic_df = create_dynamic_df(weather_json, city_id)

        engine = create_engine(connection_uri)

        with engine.connect() as conn:
            # Begin a transaction
            with conn.begin():
                # Only delete relevant rows to avoid unnecessary locking
                conn.execute(text("DELETE FROM weather_data WHERE city_id = :city_id"), {"city_id": city_id})

                # Insert new data
                dynamic_df.to_sql("weather_data", 
                                  con=conn, 
                                  if_exists="append", 
                                  index=False)
    else:
        # City does not exist; create new entries
        static_df = create_static_df(weather_json, city_name)
        city_id = static_df.iloc[0]["city_id"]
        dynamic_df = create_dynamic_df(weather_json, city_id)

        with create_engine(connection_uri).connect() as conn:
            # Add static and dynamic data
            with conn.begin():
                static_df.to_sql("city", con=conn, if_exists="append", index=False)
                dynamic_df.to_sql("weather_data", con=conn, if_exists="append", index=False)


def insert_list_of_cities(city_list):
    for city in city_list:
        insert_df(city)

def get_population():
    cities_from_sql = pd.read_sql("city", con=connection_uri)
    city_data_from_sql = pd.read_sql("weather_data", con=connection_uri)
    merged_df = pd.merge(cities_from_sql, city_data_from_sql, on='city_id', how='inner')
    result_df = merged_df[['city_name', 'population']].drop_duplicates()
    return result_df

def get_weather_for_cities():
    cities_from_sql = pd.read_sql("city", con=connection_uri)
    city_data_from_sql = pd.read_sql("weather_data", con=connection_uri)
    merged_df = pd.merge(cities_from_sql, city_data_from_sql, on='city_id', how='inner')
    return merged_df
