from typing import Any, Optional

from .metadata import MetadataBaseDoc
from src.models.routers.simulations import SimulationConfig


class SimulationConfigDB(MetadataBaseDoc, SimulationConfig):
    attached_time_series: Optional[Any]  # Binary file
