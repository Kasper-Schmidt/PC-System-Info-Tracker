from pydantic import BaseModel


class MeasurementResponse(BaseModel):
    id: int
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    measured_at: str


class SystemMeasurement(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float


class StatisticsResponse(BaseModel):
    average_cpu_usage: float
    minimum_cpu_usage: float
    maximum_cpu_usage: float

    average_memory_usage: float
    minimum_memory_usage: float
    maximum_memory_usage: float

    average_disk_usage: float
    minimum_disk_usage: float
    maximum_disk_usage: float


class AlertResponse(BaseModel):
    id: int
    measurement_id: int
    type: str
    value: float
    threshold: float
    created_at: str


class CleanupResponse(BaseModel):
    deleted_alerts: int
    deleted_measurements: int