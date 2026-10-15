
  
    

  create  table "dublin_noise"."dbt_marts"."marts_daily_Lden__dbt_tmp"
  
  
    as
  
  (
    with stage_1 as (
select * from "dublin_noise"."compute"."daily_lden"
),

stage_2 as (
select date, count(*) as flight_count
from "dublin_noise"."dbt_marts"."marts_flight_noise"
group by date)

select  stage_2.date,stage_2.flight_count,stage_1.lden
from stage_2 inner join stage_1 on stage_2.date = stage_1.date
  );
  