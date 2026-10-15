with cte_1 as (
Select *
from dbt_intermediate.int_noise_segments
where  quality_check_1 = 'actual_event'
),

cte_2 as (
select *,
	event_start at time zone 'Europe/Dublin' as start_time_local
from cte_1
),
cte_3 as (

select icao24, flight_event_number, TRIM(first_callsign) as call_sign, 
		registration, operator, model, typecode, aircraft_category ,
		operations, first_latitude, first_longitude, last_latitude, last_longitude, peak_altitude,
		time_category, manufacturer_icao, typecode, distance_m, sel,
		case  
			when sel<55 then '<55dB'
			when sel>=55 AND sel<60 then '55 - 60dB'
			when sel>=60 AND sel<65 then '60 - 65dB'
			else '+65dB' 
			END AS noise_bands,
		
	cast(start_time_local AS DATE) as date,
	EXTRACT (Hour from start_time_local) as Hours
	from cte_2),


stage_1 as (
select date, hours,operations, count(*) as flight_count, avg(sel) as sel
from cte_3
group by date,hours, operations
),

dates as (
select distinct(date) from cte_3 ),
hours as (
select generate_series(0,23) as hours
),
operations as (
select distinct(operations) from cte_3),

stage_2 as (
select * from dates cross join hours, operations
)

select stage_2.*, coalesce (stage_1.flight_count,0) as flight_count, stage_1.sel 
from stage_2 left join stage_1 
	on stage_2.date = stage_1.date 
	AND stage_2.hours = stage_1.hours
	AND stage_2.operations = stage_1.operations









