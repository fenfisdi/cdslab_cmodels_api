from typing import Any, Optional

from src.models.routes.simulations import SimulationConfig
from .metadata import MetadataBaseDoc


class SimulationConfigDB(MetadataBaseDoc, SimulationConfig):
    attached_time_series: Optional[Any]  # Binary file
