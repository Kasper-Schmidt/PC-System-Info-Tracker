import sqlite3

DATABASE_NAME = "system_info.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS system_measurements(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpu_usage REAL NOT NULL,
            memory_usage REAL NOT NULL,
            disk_usage REAL NOT NULL,
            measured_at TEXT DEFAULT CURRENT_TIMESTAMP
        )                   
    """)


    connection.execute("""
        CREATE TABLE IF NOT EXISTS alerts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            measurement_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            value REAL NOT NULL,
            threshold REAL NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (measurement_id) REFERENCES system_measurements(id)
        )
    """)

    connection.commit()
    connection.close()



def save_measurement(cpu_usage, memory_usage, disk_usage):
    connection = get_connection()

    cursor = connection.execute("""
        INSERT INTO system_measurements(
            cpu_usage,
            memory_usage,
            disk_usage
        )              
        VALUES (?, ?, ?)              
    """, (cpu_usage, memory_usage, disk_usage))

    connection.commit()
    connection.close()

    return cursor.lastrowid



def get_all_measurements():
    connection = get_connection()

    measurements = connection.execute("""
        SELECT *
        FROM system_measurements                   
    """).fetchall()

    connection.close()

    return [dict(measurement) for measurement in measurements]



def get_statistics():
    connection = get_connection()

    statistics = connection.execute("""
        SELECT
            AVG(cpu_usage) AS average_cpu_usage,
            MIN(cpu_usage) AS minimum_cpu_usage,
            MAX(cpu_usage) AS maximum_cpu_usage,
                                    
            AVG(memory_usage) AS average_memory_usage,
            MIN(memory_usage) AS minimum_memory_usage,
            MAX(memory_usage) AS maximum_memory_usage,
                                    
            AVG(disk_usage) AS average_disk_usage,
            MIN(disk_usage) AS minimum_disk_usage,
            MAX(disk_usage) AS maximum_disk_usage
        FROM system_measurements                                
    """).fetchone()

    connection.close()

    return dict(statistics)



def get_measurements_by_hours(hours):
    connection = get_connection()

    measurements  = connection.execute("""
        SELECT * 
        FROM system_measurements
        WHERE measured_at >= datetime('now', ?)                           
    """, (f"-{hours} hours",)).fetchall()

    connection.close()

    return [dict(measurement) for measurement in measurements]



def save_alert(measurement_id, type, value, threshold):
    connection = get_connection()

    connection.execute("""
        INSERT INTO alerts(
            measurement_id,
            type,
            value,
            threshold   
        )
        VALUES (?, ?, ?, ?)                   
    """, (measurement_id, type, value, threshold))

    connection.commit()
    connection.close()



def get_all_alerts():
    connection = get_connection()

    alerts = connection.execute("""
        SELECT * 
        FROM alerts                            
    """).fetchall()

    connection.close()

    return [dict(alert) for alert in alerts]



def has_recent_alert(type):
    connection = get_connection()

    alert = connection.execute("""
        SELECT *
        FROM alerts
        WHERE type = ?
        AND created_at < datetime('now', '-1 hour')                           
    """, (type,)).fetchone()

    connection.close()

    return alert is not None



def cleanup_old_data(days):
    connection = get_connection()

    cleanup_alerts = connection.execute("""
        DELETE FROM alerts
        WHERE created_at < datetime('now', ?)
    """, (f"-{days} days",)) 

    cleanup_measurements = connection.execute("""
        DELETE FROM system_measurements
        WHERE measured_at < datetime('now', ?)
    """, (f"-{days} days",))

    connection.commit()
    connection.close()

    return {
        "deleted_alerts": cleanup_alerts.rowcount,
        "deleted_measurements": cleanup_measurements.rowcount
    }