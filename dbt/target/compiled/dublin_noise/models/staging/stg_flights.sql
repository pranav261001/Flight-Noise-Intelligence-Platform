with source as (
    select * from "dublin_noise"."raw"."flight_state_vectors"
),

cleaned as (
    select
    id,
    lower(trim(icao24)) as icao24,
    trim(callsign) as callsign,
    origin_country,
    to_timestamp(time_position) as time_position,
    to_timestamp(last_contact) as last_contact,
    longitude, latitude, baro_altitude, on_ground, velocity, true_track, vertical_rate, geo_altitude,
    squawk, spi, position_source, ingestion_time
    from source
    where icao24 is not null


)

Select * from cleaned