from enum import Enum


class SimulationStatus(Enum):
    INCOMPLETE: str = 'incomplete'
    DONE: str = 'done'
    RUNNING: str = 'running'
    ERROR: str = 'error'


class ParameterType(Enum):
    FIXED: str = 'fixed'
    OPTIMIZED: str = 'optimized'


class DataSourceType(Enum):
    UPLOAD: str = 'upload'
    ISN: str = 'ins'
