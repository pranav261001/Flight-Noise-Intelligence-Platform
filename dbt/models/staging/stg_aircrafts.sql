with source as (
    select * from {{source('raw', 'aircraft_reference')}}
),
cleaned as (
    select
    lower(trim(icao24)) as icao24,
    registration, manufacturer_icao, manufacturer_name, model, typecode, icao_aircraft_type, operator, operator_icao, category_description,
    loaded_at
    from source
    where icao24 is not null


)

select * from cleaned