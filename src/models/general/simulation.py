from enum import Enum


class SimulationStatus(Enum):
    INCOMPLETE: str = 'incomplete'
    DONE: str = 'done'
    RUNNING: str = 'running'
    ERROR: str = 'error'
