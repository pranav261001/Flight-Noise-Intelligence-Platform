
  
    

  create  table "dublin_noise"."dbt_intermediate"."int_noise_segments__dbt_tmp"
  
  
    as
  
  (
    

with stage_1 as (
	select * from "dublin_noise"."dbt_intermediate"."int_flight_events"),

stage_2 as (
	select * from "dublin_noise"."compute"."noise_segments"
)

select stage_1.*, stage_2.aircraft_category, stage_2.distance_m, stage_2.sel ,stage_2.time_category 
from stage_1 LEFT JOIN stage_2 on stage_1.icao24 = stage_2.icao24 AND stage_1.flight_event_number = stage_2.flight_event
  );
  