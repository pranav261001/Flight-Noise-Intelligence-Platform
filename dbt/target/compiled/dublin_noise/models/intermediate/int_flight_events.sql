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
),

stage_2 as (

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
    group by icao24, flight_event_number),
    
stage_3 as (
    select *,
        case 
            when ping_count < 2 then 'likely_noise'
            else 'actual_event'
            end as quality_check_1,
        case 
            when first_on_ground is False and last_on_ground is True then 'Arrival'
            when first_on_ground is True and last_on_ground is False then 'Departure'
            when first_on_ground is False and last_on_ground is False then 'Overflight'
            when first_on_ground is True and last_on_ground is True then 'Ground movement'
            else null
            end as operations
    from stage_2
    )
select stage_3.*, air.registration, air.manufacturer_icao, air.manufacturer_name, air.model, air.typecode, air.icao_aircraft_type, air.operator, air.category_description

from stage_3 LEFT JOIN "dublin_noise"."dbt_staging"."stg_aircrafts" AS air
ON stage_3.icao24 = air.icao24