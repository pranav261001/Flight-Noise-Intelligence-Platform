
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select icao24
from "dublin_noise"."dbt_staging"."stg_aircrafts"
where icao24 is null



  
  
      
    ) dbt_internal_test