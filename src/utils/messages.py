from dataclasses import dataclass


@dataclass
class ModelMessage:
    updated: str = 'Model updated'
    found_all: str = 'Models founded'
    not_found_all: str = 'Models not found'
    found: str = 'Model found'
    not_found: str = 'Model not found'
    created: str = 'Model created'
    exist: str = 'Model exist'


@dataclass
class SimulationMessage:
    found: str = 'Simulation Found'
    exist: str = 'Simulation exist'
    created: str = 'Simulation created'
    not_found: str = 'Simulation not found'
    updated: str = 'Simulation updated'
    deleted: str = 'Simulation deleted'
    executing: str = 'Simulation executing'


@dataclass
class SecurityMessage:
    invalid_token: str = 'Invalid token'


@dataclass
class INSMessage:
    found: str = 'Variables found'
    not_found: str = 'Variables not found'
