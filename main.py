import datadotworld as dw
import sqlite3 as sql
import datetime, configparser

from queries import queries_create_table, query_insert_raw, query_insert_travel_times, query_insert_movement_id

if __name__ == "__main__":
    '''
    Get data from DataWorld and write to local Database
    (https://data.world/rmiller107/travel-time-uber-movement)

    documentation to configure API:
    https://docs.data.world/en/99612-configuration.html
    https://docs.data.world/en/99614-examples.html#UUID-9fbbb8b0-f5f2-7f5f-c829-7e95072c1d35
    '''
    
    status = 'RUNNING'
    print(status)

    # Read configuration variables
    config = configparser.ConfigParser()
    with open('config.cfg') as f:
        config.read_file(f)
        dataset_name = config.get('DataWorld','dataset_name')
    
    # Read tables
    datasets = dw.load_dataset(dataset_name)

    try:
        # Create DB connection
        conn = sql.connect('./sqlite.DB')
        cur = conn.cursor()

        # OPTIONAL: DROP table
        cur.execute("DROP TABLE IF EXISTS raw")
        cur.execute("DROP TABLE IF EXISTS fact_travel_times")
        cur.execute("DROP TABLE IF EXISTS dim_movement_id")

        # Create tables
        for query in queries_create_table:
            cur.execute(query)

        # Create unique index (PK) for DIM table
        query = 'create unique index pk_movement_id on dim_movement_id ( city, movement_id )'
        cur.execute(query)

        # Insert values into raw table
        for table in list(datasets.tables.keys()):
            current_data = datasets.tables[table]
            for row in current_data:
                # format columns
                keys = list(row.keys())
                columns = 'source_table,' + ','.join(keys) + ',dt_information'
                # format values
                records = tuple(row.values())
                #example: '2022-10-22 20:23:35'
                current_date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                records = (table,*records,current_date)
                query = query_insert_raw.format(columns = columns,
                                                values = records)
                query = query.replace('None','NULL')
                cur.execute(query)

        # Insert records into travel_times FACT table
        query = query_insert_travel_times
        cur.execute(query)

        # Insert records into movement_id DIM table
        query = query_insert_movement_id
        cur.execute(query)

        conn.commit()
        status = 'SUCCESS'
    except Exception as e:
        print(e)
        status = 'FAIL'
    finally:
        conn.close()
        print(status)