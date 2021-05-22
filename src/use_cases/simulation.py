import time
from io import BytesIO
from typing import List

import pandas as pd
from dinjo import ModelSEIR, ModelSEIRV, ModelSIR
from dinjo.model import Parameter, StateVariable
from scipy.integrate._ivp.ivp import OdeResult

from src.models.db import Simulation
from src.models.general import ParameterType, SimulationStatus
from src.services import FileAPI
from src.utils.date_time import DateTime


class ValidateSimulationUseCase:

    @classmethod
    def handle(cls, simulation: Simulation) -> bool:
        simulation_type = simulation.parameter_type

        if simulation_type == ParameterType.FIXED:
            # TODO: Validate Fixed Params
            pass
        elif simulation_type == ParameterType.OPTIMIZED:
            # TODO: Validate Optimized Params
            pass

        simulation.status = SimulationStatus.DONE
        simulation.save()

        return True


class ExecuteSimulationUseCase:
    @classmethod
    def handle(cls, simulation: Simulation):
        simulation_models = {
            'SIR': ModelSIR,
            'SEIR': ModelSEIR,
            'SEIRV': ModelSEIRV,
        }
        results = {}

        model_template = simulation_models.get(simulation.model.name, None)
        if not model_template:
            raise Exception("Model simulation didn't exist")

        parameters = cls.get_parameters(simulation)
        state_variables = cls.get_variable_state(simulation)

        if simulation.parameter_type == ParameterType.FIXED:
            results = cls.run_fixed_simulation(
                simulation,
                parameters,
                state_variables,
                model_template
            )
        elif simulation.parameter_type == ParameterType.OPTIMIZED:
            results = cls.run_optimized_simulation(
                simulation,
                parameters,
                state_variables,
                model_template
            )

        # cls.save_simulation(simulation, results)

    @classmethod
    def get_parameters(cls, simulation: Simulation) -> List[Parameter]:
        return [
            Parameter(
                name=parameter.label,
                representation=parameter.label,
                initial_value=parameter.value,
            ) for parameter in simulation.parameters_limits
        ]

    @classmethod
    def get_variable_state(cls, simulation: Simulation) -> List[StateVariable]:
        return [
            StateVariable(
                name=variable.label,
                representation=variable.label,
                initial_value=variable.value,
            ) for variable in simulation.state_variable_limits
        ]

    @classmethod
    def run_fixed_simulation(
        cls,
        simulation: Simulation,
        parameters: List[Parameter],
        variables: List[StateVariable],
        model_template
    ):
        # TODO: Get t_span and t_steps from simulation
        model = model_template(
            state_variables=variables,
            parameters=parameters,
            t_span=[0, 5000],
            t_steps=4999
        )
        start_time = time.time()
        results: OdeResult = model.run_model(method='RK45')
        execution_time = DateTime.format_seconds(time.time() - start_time)

        try:
            simulation.update(execution_time=execution_time)
        finally:
            simulation.reload()

        return results

    @classmethod
    def run_optimized_simulation(
        cls,
        simulation: Simulation,
        parameters: List[Parameter],
        variables: List[StateVariable],
        model_template
    ):
        response, is_invalid = FileAPI.list_simulation_files(simulation.identifier)
        if is_invalid:
            return "Retorna Error"
        files = response.get('data')

        files = [file for file in files if file.get('type') == 'upload']

        response, is_invalid = FileAPI.find_file(
            simulation.identifier,
            files[0].get('uuid')
        )

        # TODO: Verify Null Response
        df = pd.read_csv(BytesIO(response.content))

    @classmethod
    def save_simulation(cls, simulation: Simulation, results: OdeResult):
        variable_state_representation = [
            variable_state.representation for variable_state
            in simulation.state_variable_limits
        ]
        current_date = DateTime.current_datetime().isoformat()[:10]
        file_name = f'results-{current_date}.csv'

        df = pd.DataFrame(data=results.get('y')).T
        df.columns = variable_state_representation

        csv = df.to_csv(index=False)
        file_results = [('file', (file_name, csv, 'application/octet-stream'))]

        FileAPI.upload_file(
            simulation.identifier,
            files=file_results
        )
