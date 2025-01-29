-- Drop the database if it already exists
DROP DATABASE IF EXISTS scooter_grab ;

-- Create the database
CREATE DATABASE scooter_grab;

-- Use the database
USE scooter_grab;

CREATE TABLE city (
    city_id VARCHAR(255) UNIQUE NOT NULL,
    city_name VARCHAR(255) NOT NULL,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    country VARCHAR(255),
    PRIMARY KEY (city_id)
);


CREATE TABLE weather_data (
    data_id VARCHAR(255) UNIQUE NOT NULL,
    population INT,
    timestamp DATETIME NOT NULL,
    temperature FLOAT NOT NULL,
    feels_like FLOAT NOT NULL,
    humidity INT NOT NULL,
    wind_speed FLOAT NOT NULL,
    sky VARCHAR(255),
    sunrise INT NOT NULL,
    sunset INT NOT NULL,
    city_id VARCHAR(255) NOT NULL,
    PRIMARY KEY (data_id),
    FOREIGN KEY (city_id) REFERENCES city(city_id)
);


CREATE TABLE airports (
    airport_id VARCHAR(255) NOT NULL,
    icao VARCHAR(10) NOT NULL,
    iata VARCHAR(10) NOT NULL,
    airport_name VARCHAR(255) NOT NULL,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    city_id VARCHAR(255) NOT NULL,
    PRIMARY KEY (airport_id),
    FOREIGN KEY (city_id) REFERENCES city(city_id)
);


CREATE TABLE arrivals_data (
    flight_id VARCHAR(255) NOT NULL,
    scheduledTime DATETIME NOT NULL,
    flight_number VARCHAR(20) NOT NULL,
    status VARCHAR(255) NOT NULL,
    airline_name VARCHAR(255) NOT NULL,
    arrival_airport_icao VARCHAR(10) NOT NULL,
    departure_airport_icao VARCHAR(10) NOT NULL,
    airport_id VARCHAR(255) NOT NULL,
    PRIMARY KEY (flight_id),
    FOREIGN KEY (airport_id) REFERENCES airports(airport_id)
);


SELECT *
FROM city;

SELECT *
FROM weather_data;

SELECT *
FROM airports;

SELECT *
FROM arrivals_data;