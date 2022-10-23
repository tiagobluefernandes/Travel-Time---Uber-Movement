query_create_table_raw = """
CREATE TABLE IF NOT EXISTS raw (
    source_table string,
    origin_movement_id int,
    origin_display_name string,
    origin_geometry string,
    destination_movement_id int,
    destination_display_name string,
    destination_geometry string,
    date_range string,
    mean_travel_time_seconds int,
    range_lower_bound_travel_time_seconds int,
    range_upper_bound_travel_time_seconds int,
    dt_information datetime
    );
    """

query_create_table_travel_times = """
CREATE TABLE IF NOT EXISTS fact_travel_times (
    city string,
    origin_movement_id int,
    destination_movement_id int,
    date_range_start date,
    date_range_end date,
    date_range_frequency string,
    date_range_agg_method string,
    mean_travel_time_seconds int,
    range_lower_bound_travel_time_seconds int,
    range_upper_bound_travel_time_seconds int,
    dt_information datetime
    );
    """

query_create_table_movement_id = """
CREATE TABLE IF NOT EXISTS dim_movement_id (
    city string,
    movement_id int,
    display_name string,
    geometry string,
    dt_information datetime
    );
    """

query_insert_raw = """
INSERT INTO raw ({columns})
    VALUES {values};
"""

query_insert_travel_times = """
INSERT INTO fact_travel_times (
        city,
        origin_movement_id,
        destination_movement_id,
        date_range_start,
        date_range_end,
        date_range_frequency,
        date_range_agg_method,
        mean_travel_time_seconds,
        range_lower_bound_travel_time_seconds,
        range_upper_bound_travel_time_seconds,
        dt_information
        )
    SELECT 
        replace(raw.source_table,'travel_times_','') as city,
        raw.origin_movement_id,
        raw.destination_movement_id,
        (select date(substr(raw.date_range,7,4) || '-' || substr(raw.date_range,1,2) || '-' || substr(raw.date_range,4,2))) as date_range_start,
        (select date(substr(raw.date_range,20,4) || '-' || substr(raw.date_range,14,2) || '-' || substr(raw.date_range,17,2))) as date_range_end,
        (select trim(
            substr(
                raw.date_range,                                                        /* raw data */
                instr(raw.date_range,',')+1,                                           /* first comma */
                instr(substr(raw.date_range,instr(raw.date_range,', ')+1),',')-1),     /* length to second comma after first */
            ' ')) as date_range_frequency,
        (select trim(
            substr(
                raw.date_range,
                instr(raw.date_range,',') + instr(substr(raw.date_range,instr(raw.date_range,', ')+1),',')+1),         /* length to first comma + length to second comma*/
            " ")) as date_range_agg_method,
        raw.mean_travel_time_seconds,
        raw.range_lower_bound_travel_time_seconds,
        raw.range_upper_bound_travel_time_seconds,
        DATETIME('now','localtime') as dt_information
    FROM raw
    ;
"""

query_insert_movement_id = """
INSERT OR REPLACE INTO dim_movement_id (
    city,
    movement_id,
    display_name,
    geometry,
    dt_information
    )
    SELECT DISTINCT
        replace(raw.source_table,'travel_times_','') as city,
        raw.origin_movement_id as movement_id,
        raw.origin_display_name as display_name,
        raw.origin_geometry as geometry,
        DATETIME('now','localtime') as dt_information
    FROM raw
    UNION
    SELECT DISTINCT
        replace(raw.source_table,'travel_times_','') as city,
        raw.destination_movement_id as movement_id,
        raw.destination_display_name as display_name,
        raw.destination_geometry as geometry,
        DATETIME('now','localtime') as dt_information
    FROM raw
    ;
"""

queries_create_table = [
    query_create_table_raw,
    query_create_table_travel_times,
    query_create_table_movement_id]
    