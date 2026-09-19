
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    icao24 as unique_field,
    count(*) as n_records

from "dublin_noise"."dbt_staging"."stg_aircrafts"
where icao24 is not null
group by icao24
having count(*) > 1



  
  
      
    ) dbt_internal_test