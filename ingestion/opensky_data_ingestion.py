import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text #( required for database connection, create engine, and execute queries)
from dotenv import load_dotenv
import urllib
url =  "https://opensky-network.org/api/states/all"

# response = requests.get(url)



columns = ["icao24", "callsign", "origin_country", "time_position", "last_contact",
           "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
           "true_track", "vertical_rate", "sensors", "geo_altitude",
           "squawk", "spi", "position_source"]

# data = response.json()['states']
# df = pd.DataFrame(data, columns=columns)
# print(df.head())

# LAMIN, LAMAX = 53.39, 53.46
# LOMIN, LOMAX = -6.30, -6.15

# params = {'lamin': LAMIN, 'lamax': LAMAX, 'lomin': LOMIN, 'lomax': LOMAX}
# resposne = requests.get(url=url, params=params, timeout=30)
# data = resposne.json()['states']
# df = pd.DataFrame(data, columns=columns)
# print(df.head())



load_dotenv()

# Database connection parameters
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# print(DB_PORT, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

OPEN_SKY_USER = os.getenv('OPEN_SKY_USER')
OPEN_SKY_PASSWORD = os.getenv('OPEN_SKY_PASS')

encoded_password = urllib.parse.quote_plus(DB_PASSWORD) #---- Error solved: password with special characters needs to be URL-encoded

def get_engine():
    return (
        create_engine(f"postgresql+psycopg2://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    )

def create_raw_schema(engine):
    with engine.begin() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        connection.execute(text("""
    CREATE TABLE IF NOT EXISTS raw.flight_state_vectors (
        "id" SERIAL PRIMARY KEY,
        "icao24" VARCHAR(255),
        "callsign" VARCHAR(255),
        "origin_country" VARCHAR(255),
        "time_position" BIGINT,
        "last_contact" BIGINT,
        "longitude" FLOAT,
        "latitude" FLOAT,
        "baro_altitude" FLOAT,
        "on_ground" BOOLEAN,
        "velocity" FLOAT,
        "true_track" FLOAT,
        "vertical_rate" FLOAT,
        "sensors" VARCHAR(255),
        "geo_altitude" FLOAT,
        "squawk" VARCHAR(255),
        "spi" BOOLEAN,
        "position_source" INTEGER,
        "ingestion_time" TIMESTAMP DEFAULT Now()
        );                
                                 """))
 

LAMIN, LAMAX = 53.1, 53.7
LOMIN, LOMAX = -6.7, -5.9

def fetch_flight_data():
    params = {'lamin': LAMIN, 'lamax': LAMAX, 'lomin': LOMIN, 'lomax': LOMAX}
    response = requests.get(url=url, params=params, auth=(OPEN_SKY_USER, OPEN_SKY_PASSWORD), timeout=30)
    response.raise_for_status()  # Check if the request was successful
    return response.json().get('states', [])  # Return the 'states' data or an empty list if not found

def parse_states(states):
    df = pd.DataFrame(states, columns=columns)
    df["callsign"] = df["callsign"].str.strip()
    df["sensors"] = df["sensors"].apply(lambda x: str(x) if x is not None else None)
    return df

def save_to_db(df, engine):
    df.to_sql(
        name ="flight_state_vectors",
        schema = "raw",
        con=engine,
        if_exists='append',
        index=False,
    )

def run():
    engine = get_engine()
    create_raw_schema(engine)
    print("Fetchining flight data from opnesky API...")
    states = fetch_flight_data()
    if not states:
        print("No flight data found in the specified area.")
        return 

    df = parse_states(states)
    print(f"Fetched {len(df)} flights. saving to the database")
    save_to_db(df, engine)
    print(f"Done!")

if __name__ == "__main__":
    run()