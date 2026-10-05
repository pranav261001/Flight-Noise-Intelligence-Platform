from estimator import period_leq, lden
import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text #( required for database connection, create engine, and execute queries)
from dotenv import load_dotenv
import urllib


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
    df = pd.read_sql("select * from compute.noise_segments", engine)
    return df


engine = get_engine()
df = load_flight(engine)

# print(df.head())


df_2 = df.groupby(['start_date', 'time_category'])   
df_sel_list = pd.DataFrame(df_2['sel'].apply(list).reset_index())

SECONDS = {
    'Day' : 43200,
    'Eve' : 14400,
    'Night' : 28800
}

# print(SECONDS['Day'])

# for date, date_rows in df_sel_list.groupby('start_date'):
#     for index, row in date_rows.iterrows():
#         print(index)


def compute_lden(df):
    compute_2 = [ ]

    for date, date_rows in df.groupby('start_date'):
        ld = period_leq([], SECONDS['Day'])
        le = period_leq([], SECONDS['Eve'])
        ln = period_leq([], SECONDS['Night'])

        for index, row in date_rows.iterrows():

            if row['time_category'] == "Day":
                ld = period_leq(row['sel'], SECONDS['Day'])
            elif row['time_category'] == "Evening":
                le = period_leq(row['sel'], SECONDS['Eve'])
            elif row['time_category'] == "Night":
                ln = period_leq(row['sel'], SECONDS['Night'])

        Lden_val = lden(ld, le, ln)

        compute_2.append({
            'date': date,
            'ld' : ld,
            'le' : le,
            'ln' : ln,
            'lden': Lden_val
        })
    return compute_2

data = compute_lden(df_sel_list)
data_2 = pd.DataFrame(data)

print(data_2)



def create_compute_schema(engine):
    with engine.begin() as connection:
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS compute;"))
        connection.execute(text("""
    CREATE TABLE IF NOT EXISTS compute.daily_lden (
        "date" DATE,
        "ld" FLOAT,
        "le" FLOAT,
        "ln" FLOAT,
        "lden" FLOAT
        ); """))
def save_to_db(df, engine):
    df.to_sql(
        name="daily_lden",
        schema = "compute",
        con=engine,
        if_exists = 'replace',
        index=False
    )

def run(df):
    engine = get_engine()
    create_compute_schema(engine)
    save_to_db(df, engine)
    print("Done!")

run(data_2)
