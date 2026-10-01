import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text #( required for database connection, create engine, and execute queries)
from dotenv import load_dotenv
import urllib
from estimator import classify_aircrafts, haversine_formula, period_leq, lden, time_bucket, sel_estimate, slant_distance 

load_dotenv()

# Database connection parameters
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


OPEN_SKY_USER = os.getenv('OPEN_SKY_USER')
OPEN_SKY_PASSWORD = os.getenv('OPEN_SKY_PASS')

encoded_password = urllib.parse.quote_plus(DB_PASSWORD) #---- Error solved: password with special characters needs to be URL-encoded

def get_engine():
    return (
        create_engine(f"postgresql+psycopg2://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

    )

def load_flight(engine):
    df = pd.read_sql("SELECT * FROM dbt_intermediate.int_flight_events", engine)
    return df


engine = get_engine()
df = load_flight(engine)
# print(df.isnull().sum())



def compute_noise_segments(df):
    Compute = [ ]
    for index, row in df.iterrows():
        icao = row['icao24']
        flight_event = row['flight_event_number']
        category = classify_aircrafts(row['typecode'], row['icao_aircraft_type'], row['category_description'])
        d1 = slant_distance(row['first_latitude'], row['first_longitude'],row['first_altitude'])
        d2 = slant_distance(row['last_latitude'], row['last_longitude'],row['last_altitude'])
        distance = min(d1,d2)
        sel = sel_estimate(category, distance)
        time = time_bucket(row['event_start'])       
    
        Compute.append({
            'icao24': icao,
            'Flight_Event': flight_event,
            'Aircraft_Category': category,
            'Distance_m': distance,
            'SEL':sel,
            'Time_Category': time
        })
    return Compute

computed = compute_noise_segments(df)

computed_data = pd.DataFrame(computed)
print(computed_data.head())


def create_compute_schema(engine):
    with engine.begin() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS compute;"))
        connection.execute(text("""
    CREATE TABLE IF NOT EXISTS compute.noise_segments (
        "icao24" VARCHAR(255),
        "Flight_Event" BIGINT,
        "Aircraft_Category" VARCHAR(255),
        "Distance_m" FLOAT,
        "SEL" FLOAT,
        "Time_Category" VARCHAR(255)
        ); """))
def save_to_db(df, engine):
    df.to_sql(
        name="noise_segments",
        schema = "compute",
        con=engine,
        if_exists = 'append',
        index=False
    )

def run(df):
    engine = get_engine()
    create_compute_schema(engine)
    save_to_db(df, engine)
    print("Done!")

run(computed_data)


