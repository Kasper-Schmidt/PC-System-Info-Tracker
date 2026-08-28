import psutil
import asyncio

from .database import save_measurement, save_alert, has_recent_alert
from .schemas import SystemMeasurement

def measure_system():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("C:\\").percent

    return SystemMeasurement(
        cpu_usage=cpu_usage,
        memory_usage=memory_usage,
        disk_usage=disk_usage
    )



def check_alerts(measurement_id: int, measurement: SystemMeasurement):
    threshold = 90

    if measurement.cpu_usage > threshold:
        if not has_recent_alert():
            save_alert(measurement_id, "CPU", measurement.cpu_usage, threshold)

    if measurement.memory_usage > threshold:
        if not has_recent_alert():
            save_alert(measurement_id, "Memory", measurement.memory_usage, threshold)

    if measurement.disk_usage > threshold:
        if not has_recent_alert():
            save_alert(measurement_id, "Disk", measurement.disk_usage, threshold)



async def start_monitoring():
    while True:
        measurement = measure_system()

        measurement_id = save_measurement(
            measurement.cpu_usage,
            measurement.memory_usage,
            measurement.disk_usage
        )

        check_alerts(measurement_id, measurement)

        await asyncio.sleep(60 * 15)




