import time
from io import BytesIO
from typing import List

import pandas as pd
from dinjo.model import Parameter, StateVariable
from dinjo.optimizer import Optimizer
from dinjo.predefined.epidemiology import ModelSEIR, ModelSEIRV, ModelSIR
from pandas import DataFrame

from src.models.db import Simulation
from src.models.general import ParameterType
from src.services import FileAPI
from src.utils.date_time import DateTime


class ExecuteSimulationUseCase:
    @classmethod
    def handle(cls, simulation: Simulation):
        simulation_models = {
            'SIR': ModelSIR,
            'SEIR': ModelSEIR,
            'SEIRV': ModelSEIRV,
        }
        days = DateTime.get_delta_days(
            simulation.interval_date.start,
            simulation.interval_date.end
        )
        range_days = [0, days - 1]

        model_template = simulation_models.get(simulation.model.name, None)
        if not model_template:
            raise RuntimeError("Model simulation didn't exist")

        parameters = cls.get_parameters(simulation)
        state_variables = cls.get_variable_state(simulation)

        model = model_template(
            state_variables=state_variables,
            parameters=parameters,
            t_span=range_days,
            t_steps=days
        )

        start_time = time.time()
        results = model.run_model(method='RK45')
        if simulation.parameter_type == ParameterType.OPTIMIZED:

            variable_to_fit = next((
                variable for variable in simulation.state_variable_limits
                if variable.to_fit
            ), None)
            assert variable_to_fit, "Undefined"

            variable_model = next((
                variable for variable in state_variables
                if variable.name == variable_to_fit.representation
            ), None)

            file = cls.get_upload_file(simulation)
            reference_values = file[variable_to_fit.representation].to_numpy()

            # TODO: Verify Args for Optimization object
            algorithm_kwargs = {
                'popsize': 20,
                'disp': True,
                'tol': 0.0015,
                'maxiter': 100,
                'mutation': [0.3, 0.7],
                'atol': 200
            }

            optimizer = Optimizer(
                model=model,
                reference_state_variable=variable_model,
                reference_values=reference_values,
                reference_t_values=results.t
            )

            optimal = optimizer.optimize(
                cost_method='root_mean_square',
                algorithm='differential_evolution',
                algorithm_kwargs=algorithm_kwargs
            )
            optimized_params = optimal.x

            # Update Params
            for index in range(len(parameters)):
                parameters[index].initial_value = optimized_params[index]

            # Update Model simulation
            optimized_mode = model_template(
                state_variables=state_variables,
                parameters=parameters,
                t_span=range_days,
                t_steps=days
            )

            results = optimized_mode.run_model(method='RK45')

        end_time = DateTime.format_seconds(time.time() - start_time)

        try:
            simulation.update(execution_time=end_time)
        finally:
            simulation.reload()

        cls.save_simulation(simulation, results)

    @classmethod
    def get_parameters(cls, simulation: Simulation) -> List[Parameter]:
        parameters = []

        for parameter in simulation.parameters_limits:
            is_optimized = parameter.type == ParameterType.OPTIMIZED
            value = parameter.value if parameter.value else 0
            bounds = [value, value]

            if is_optimized:
                min_value, max_value = parameter.min_value, parameter.max_value
                bounds = [min_value, max_value]
                value = min_value

            parameters.append(
                Parameter(
                    name=parameter.label,
                    representation=parameter.label,
                    initial_value=value,
                    bounds=bounds
                )
            )

        return parameters

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
    def get_upload_file(cls, simulation: Simulation) -> DataFrame:
        response, is_invalid = FileAPI.list_simulation_files(
            simulation.identifier
        )
        if is_invalid:
            raise RuntimeError('Cannot find folder file')

        data = response.get('data')
        upload_files = [file for file in data if file.get('type') == 'upload']
        file = upload_files[0]

        response, is_invalid = FileAPI.find_file(
            simulation.identifier,
            file.get('uuid')
        )
        if is_invalid:
            raise RuntimeError('Cannot find file')

        return pd.read_csv(BytesIO(response.content))

    @classmethod
    def save_simulation(cls, simulation: Simulation, results):
        interval = DateTime.create_date_range(
            simulation.interval_date.start,
            simulation.interval_date.end
        )
        variable_state_representation = [
            variable_state.label for variable_state
            in simulation.state_variable_limits
        ]
        current_date = DateTime.current_datetime().isoformat()[:10]
        file_name = f'results-{current_date}.csv'

        df = pd.DataFrame(data=results.get('y')).T
        df.columns = variable_state_representation
        df.index = interval

        csv = df.to_csv(index=True, header=True)
        file_results = [('file', (file_name, csv, 'application/octet-stream'))]

        FileAPI.upload_file(
            simulation.identifier,
            files=file_results
        )
