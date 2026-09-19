
  create view "dublin_noise"."dbt_intermediate"."int_flight_events__dbt_tmp"
    
    
  as (
    with stage_1 as (
Select *,
    FIRST_VALUE(on_ground) OVER(PARTITION BY icao24, flight_event_number ORDER BY last_contact) as first_on_ground,
	LAST_VALUE(on_ground) OVER(PARTITION BY icao24, flight_event_number ORDER BY last_contact ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_on_ground,
	FIRST_VALUE(baro_altitude) OVER(PARTITION BY icao24, flight_event_number ORDER BY last_contact) as first_altitude,
	LAST_VALUE(baro_altitude) OVER(PARTITION BY icao24, flight_event_number ORDER BY last_contact ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_altitude,
	FIRST_VALUE(latitude) OVER(PARTITION BY icao24, flight_event_number ORDER BY last_contact) as first_latitude,
	FIRST_VALUE(longitude) OVER(PARTITION BY icao24, flight_event_number ORDER BY last_contact) as first_longitude,
	LAST_VALUE(latitude) OVER(PARTITION BY icao24, flight_event_number ORDER BY last_contact ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_latitude,
	LAST_VALUE(longitude) OVER(PARTITION BY icao24, flight_event_number ORDER BY last_contact ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_longitude,
	LAST_VALUE(true_track) OVER(PARTITION BY icao24, flight_event_number ORDER BY last_contact ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_heading,
	FIRST_VALUE(callsign) OVER(PARTITION BY icao24, flight_event_number ORDER BY last_contact) as first_callsign	

from "dublin_noise"."dbt_intermediate"."int_flight_pings_rank" 
)

select
	icao24,flight_event_number, 
	min(last_contact) as event_start,
	max(last_contact) as event_end,
	max(baro_altitude) as peak_altitude,
	count(*) as ping_count,
	max(first_altitude) as first_altitude,
	max(last_altitude) as last_altitude,

	max(first_latitude) as first_latitude,
    max(last_latitude) as last_latitude,

    max(first_longitude) as first_longitude,
    max(last_longitude) as last_longitude,

    max(last_heading) as last_heading,

    max(first_callsign) as first_callsign,
	
	bool_or(first_on_ground) as first_on_ground,
    bool_or(last_on_ground) as last_on_ground
	
from stage_1
group by icao24, flight_event_number
  );