from dataclasses import dataclass


@dataclass
class ModelMessage:
    found_all: str = 'Models founded'
    not_found_all: str = 'Models not found'
    found: str = 'Model found'
    not_found: str = 'Model not found'
    created: str = 'Model Created'


@dataclass
class SimulationMessage:
    found: str = 'Simulation Found'
    exist: str = 'Simulation exist'
    created: str = 'Simulation created'
    not_found: str = 'Simulation not found'


@dataclass
class SecurityMessage:
    invalid_token: str = 'Invalid token'
