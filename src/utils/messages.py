from dataclasses import dataclass


@dataclass
class ModelMessage:
    """
    Messages used in endpoint responses for models 
    """
    updated: str = 'Model updated'
    found_all: str = 'Models founded'
    not_found_all: str = 'Models not found'
    found: str = 'Model found'
    not_found: str = 'Model not found'
    created: str = 'Model created'
    exist: str = 'Model exist'


@dataclass
class SimulationMessage:
    """
    Messages used in endpoint responses for Simulations
    """
    found: str = 'Simulation Found'
    exist: str = 'Simulation exist'
    created: str = 'Simulation created'
    not_found: str = 'Simulation not found'
    updated: str = 'Simulation updated'
    deleted: str = 'Simulation deleted'


@dataclass
class SecurityMessage:
    """
    Messages used in endpoint responses for security
    """
    invalid_token: str = 'Invalid token'
