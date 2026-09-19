import schedule
import time

from opensky_data_ingestion import run


def data_inqestion_task():
    try:

        run() 
        print(f"Fetched and Ingested data on {time.ctime()}")
    except Exception as e:
        print(f"Data cannot be ingested because of the Error: {e}")

schedule.every(60).seconds.do(data_inqestion_task)

while (1):
    schedule.run_pending()
    time.sleep(1)

