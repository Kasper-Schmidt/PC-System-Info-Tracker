from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from .database import create_database, get_all_measurements, get_statistics, get_measurements_by_hours, get_all_alerts, cleanup_old_data
from .monitor import start_monitoring, measure_system, check_alerts
from .schemas import MeasurementResponse, SystemMeasurement, StatisticsResponse, AlertResponse, CleanupResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(start_monitoring())

    yield

    task.cancel()


app = FastAPI(
    title="System info tracker",
    description="This program will save my PC information in a database",
    lifespan=lifespan
)


create_database()


@app.get("/")
def root():
    return {
        "message": "System Info Tracker is runnning!"
    }


@app.get("/system/history", response_model=list[MeasurementResponse])
def measurement_history():
    return get_all_measurements()


@app.get("/system/history/filter", response_model=list[MeasurementResponse])
def get_filtered_history(hours: int):
    return get_measurements_by_hours(hours)


@app.get("/system/current", response_model=SystemMeasurement)
def current_measurement():
    return measure_system()


@app.get("/system/statistics", response_model=StatisticsResponse)
def statistics():
    return get_statistics()

@app.get("/system/alerts", response_model=list[AlertResponse])
def alert():
    return get_all_alerts()


@app.delete("/system/cleanup", response_model=CleanupResponse)
def cleanup(days: int):
    return cleanup_old_data(days)

