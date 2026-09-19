
  create view "dublin_noise"."dbt_intermediate"."int_flight_pings_rank__dbt_tmp"
    
    
  as (
    with ranked as (
    select
    icao24, callsign, 
    last_contact, LAG(last_contact, 1,null) OVER(PARTITION BY icao24 ORDER BY last_contact) as Previous_contact,
    longitude, latitude, baro_altitude, geo_altitude, on_ground, vertical_rate, velocity, true_track
    from "dublin_noise"."dbt_staging"."stg_flights"),

ranked_2 as (
select *, 
	 extract(epoch from (last_contact - previous_contact)) / 60 as gap_minutes
			
from ranked),

ranked_3 as(
select *, 
	case 
		when previous_contact is null then 1
		when gap_minutes > 10 then 1
		else 0 
		end as new_event	
from ranked_2)

select *,
    sum(new_event) OVER(PARTITION BY icao24 ORDER BY last_contact) as flight_event_number


from ranked_3
  );