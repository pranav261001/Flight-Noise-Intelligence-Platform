import io

import pandas as pd
import requests
from sqlalchemy import text

from opensky_data_ingestion import get_engine

AIRCRAFT_DB_URL = "https://opensky-network.org/datasets/metadata/aircraftDatabase.csv"

# Source column name -> destination column name
COLUMNS = {
    "icao24": "icao24",
    "registration": "registration",
    "manufacturericao": "manufacturer_icao",
    "manufacturername": "manufacturer_name",
    "model": "model",
    "typecode": "typecode",
    "icaoaircrafttype": "icao_aircraft_type",
    "operator": "operator",
    "operatoricao": "operator_icao",
    "categoryDescription": "category_description",
}


def create_reference_schema(engine):
    with engine.begin() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS raw;"))
        connection.execute(text("""
    CREATE TABLE IF NOT EXISTS raw.aircraft_reference (
        "icao24" VARCHAR(50) PRIMARY KEY,
        "registration" VARCHAR(20),
        "manufacturer_icao" VARCHAR(50),
        "manufacturer_name" VARCHAR(255),
        "model" VARCHAR(255),
        "typecode" VARCHAR(50),
        "icao_aircraft_type" VARCHAR(50),
        "operator" VARCHAR(255),
        "operator_icao" VARCHAR(50),
        "category_description" VARCHAR(255),
        "loaded_at" TIMESTAMP DEFAULT NOW()
        );
                                 """))


def fetch_aircraft_reference():
    response = requests.get(AIRCRAFT_DB_URL, timeout=120)
    response.raise_for_status()
    df = pd.read_csv(io.StringIO(response.text), usecols=list(COLUMNS.keys()), low_memory=False)
    df = df.rename(columns=COLUMNS)
    df["icao24"] = df["icao24"].str.strip().str.lower()
    df = df.dropna(subset=["icao24"]).drop_duplicates(subset=["icao24"])
    return df


def save_to_db(df, engine):
    with engine.begin() as connection:
        connection.execute(text("TRUNCATE TABLE raw.aircraft_reference;"))
        df.to_sql(
            name="aircraft_reference",
            schema="raw",
            con=connection,
            if_exists="append",
            index=False,
        )


def run():
    engine = get_engine()
    create_reference_schema(engine)
    print("Fetching aircraft reference data from OpenSky...")
    df = fetch_aircraft_reference()
    print(f"Fetched {len(df)} aircraft records. Saving to the database...")
    save_to_db(df, engine)
    print("Done!")


if __name__ == "__main__":
    run()
