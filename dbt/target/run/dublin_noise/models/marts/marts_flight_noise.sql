
  
    

  create  table "dublin_noise"."dbt_marts"."marts_flight_noise__dbt_tmp"
  
  
    as
  
  (
    with cte_1 as (
Select *
from "dublin_noise"."dbt_intermediate"."int_noise_segments"
where  quality_check_1 = 'actual_event'
),

cte_2 as (
select *,
	event_start at time zone 'Europe/Dublin' as start_time_local
from cte_1
)

select icao24, flight_event_number, TRIM(first_callsign) as call_sign, 
		registration, operator, model, typecode, aircraft_category ,
		operations, first_latitude, first_longitude, last_latitude, last_longitude, peak_altitude,
		time_category, manufacturer_icao, distance_m, sel,
		case  
			when sel<55 then '<55dB'
			when sel>=55 AND sel<60 then '55 - 60dB'
			when sel>=60 AND sel<70 then '60 - 70dB'
            when sel>=70 AND sel<80 then '70 - 80dB'
            when sel>=80 AND sel<90 then '80 - 90dB'
			else '+90dB' 
			END AS noise_bands,
		
	cast(start_time_local AS DATE) as date,
	EXTRACT (Hour from start_time_local) as Hours
	from cte_2

-- 60–70, 70–80, 80–90, 90+ dB
  );
  