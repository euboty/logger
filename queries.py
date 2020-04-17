# Wieviel Uhr soll die Grenze liegen?
critical_hour = 3
# Which temperature counts as SAUNA = ON
critical_temperature = 40


def get_last_temp(curs):
    curs.execute("""
        SELECT timestamp, temp
        FROM temps
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    last_entry = curs.fetchone()
    return last_entry["temp"]


def get_last_vibration(curs):
    curs.execute("""
        SELECT timestamp, vibration
        FROM vibrations
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    last_entry = curs.fetchone()
    return last_entry["vibration"]


def get_sauna_dates(curs):
    curs.execute(f"""
        WITH sauna_with_critical_hour_shift as (
            SELECT
                date(
                    datetime(timestamp, 'unixepoch','localtime', '-{critical_hour} hours')
                ) as day_shifted
                , temp
            FROM temps
            WHERE timestamp >= strftime('%s', 'now', '-30 day')
        )
        SELECT day_shifted
        FROM sauna_with_critical_hour_shift
        WHERE temp > {critical_temperature}
        GROUP BY day_shifted
    """)
    sauna_date_rows = list(curs.fetchall())
    return [row["day_shifted"] for row in sauna_date_rows]


def get_pool_dates(curs):
    curs.execute(f"""
        WITH pool_with_critical_hour_shift as (
            SELECT
                date(
                    datetime(timestamp, 'unixepoch', 'localtime', '-{critical_hour} hours')
                ) as day_shifted
                , vibration
            FROM vibrations
            WHERE timestamp >= strftime('%s', 'now', '-30 day')
        )
        SELECT day_shifted
        FROM pool_with_critical_hour_shift
        WHERE vibration is TRUE
        GROUP BY day_shifted
    """)
    pool_date_rows = list(curs.fetchall())
    return [row["day_shifted"] for row in pool_date_rows]


def get_sauna_day_data(curs, day):
    """
    returns all temperatures and timestamps of one day starting at critical_hour
    """
    curs.execute(f"""
        SELECT timestamp, temp
        FROM temps
        --where timestamp in range of 3AM of the wanted day till 3AM the next day
        WHERE strftime('%Y-%m-%d', timestamp, 'unixepoch', '-{critical_hour} hours') = '{day}'
        ORDER BY timestamp ASC
    """)

    dates = []
    temps = []
    for data in curs.fetchall():
        dates.append(data["timestamp"])
        temps.append(data["temp"])
    return (dates, temps)


def get_pool_day_data(curs, day):
    """
    returns all vibrations and timestamps of one day starting at critical_hour
    """
    curs.execute(f"""
        SELECT timestamp, vibration
        FROM vibrations
        --where timestamp in range of 3AM of the wanted day till 3AM the next day
        WHERE strftime('%Y-%m-%d', timestamp, 'unixepoch', '-{critical_hour} hours') = '{day}'
        ORDER BY timestamp ASC
    """)

    dates = []
    vibrations = []
    for data in curs.fetchall():
        dates.append(data["timestamp"])
        vibrations.append(data["vibration"])
    return (dates, vibrations)


def get_sauna_week_data(curs):
    """
    returns all temperatures and timestamps of the last 7 days
    """
    curs.execute("""
        SELECT timestamp, temp
        FROM temps
        WHERE timestamp >= strftime('%s', 'now', 'localtime', '-7 day')
        ORDER BY timestamp ASC
    """)
    dates = []
    temps = []
    for data in curs.fetchall():
        dates.append(data["timestamp"])
        temps.append(data["temp"])
    return (dates, temps)


def get_pool_week_data(curs):
    """
    returns all vibrations and timestamps of the last 7 days
    """
    curs.execute("""
        SELECT timestamp, vibration
        FROM vibrations
        WHERE timestamp >= strftime('%s', 'now', 'localtime', '-7 day')
        ORDER BY timestamp ASC
    """)
    dates = []
    vibrations = []
    for data in curs.fetchall():
        dates.append(data["timestamp"])
        vibrations.append(data["vibration"])
    return (dates, vibrations)


# def get_pool_day_minutes(curs, day):
#         """
#     returns sum of minutes with vibration of one day starting at critical_hour
#     """
#     curs.execute(f"""
#         SELECT timestamp, vibration
#         FROM vibrations
#         --where timestamp in range of 3AM of the wanted day till 3AM the next day
#         WHERE timestamp
#             BETWEEN datetime('{day}', '+{critical_hour} hours')
#             AND datetime('{day}', '+1 day', '+{critical_hour} hours')
#         ORDER BY timestamp ASC
#     """)

#     dates = []
#     vibrations = []
#     for data, in curs.fetchall():
#         dates.append(data["timestamp"])
#         vibrations.append(data["vibration"])

#     # starting at -5min so the first vibration is minute 0
#     minute_sum = -5
#     for date, vibration in zip(dates, vibrations):
#         if vibration == True:
#             minute_sum = minute_sum + 5
#     return (minute_sum)
