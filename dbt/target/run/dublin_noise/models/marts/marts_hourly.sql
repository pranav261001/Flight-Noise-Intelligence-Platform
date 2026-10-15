
  
    

  create  table "dublin_noise"."dbt_marts"."marts_hourly__dbt_tmp"
  
  
    as
  
  (
    with stage_1 as (
select date, hours,operations, count(*) as flight_count, avg(sel) as avg_sel
from "dublin_noise"."dbt_marts"."marts_flight_noise"
group by date,hours, operations
),

dates as (
select distinct(date) from "dublin_noise"."dbt_marts"."marts_flight_noise" ),
hours as (
select generate_series(0,23) as hours
),
operations as (
select distinct(operations) from "dublin_noise"."dbt_marts"."marts_flight_noise"),

stage_2 as (
select * from dates cross join hours, operations
)

select stage_2.*, coalesce(stage_1.flight_count,0) as flight_count, stage_1.avg_sel 
from stage_2 left join stage_1 
	on stage_2.date = stage_1.date 
	AND stage_2.hours = stage_1.hours
	AND stage_2.operations = stage_1.operations
  );
  