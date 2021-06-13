from itertools import cycle
from typing import List, Optional

from dinjo.model import StateVariable
from pandas import DataFrame
from plotly.express.colors import qualitative
from plotly.graph_objects import Layout
from plotly.graph_objs import Figure, Scatter


class GraphUseCase:
    palette = cycle(qualitative.Antique)

    @classmethod
    def create_general_figure(
        cls,
        df: DataFrame,
        is_optimized: bool,
        variable_state: Optional[StateVariable] = None
    ) -> List[Figure]:

        figures = []
        scatter_options = dict(
            mode='lines',
            connectgaps=False,
        )
        x = df[df.columns[0]].to_list()

        main_layout = Layout(
            title="Time Series Prediction",
            xaxis_title="Date",
            yaxis_title="Persons"
        )
        main_figure = Figure(layout=main_layout)

        start_range = 2 if is_optimized else 1
        finish_range = len(df.columns[start_range:]) + start_range

        for i in range(start_range, finish_range):
            layout = Layout(
                title=f"{df.columns[i]} Time Series",
                xaxis_title="Date",
                yaxis_title="Persons"
            )
            fig = Figure(layout=layout)
            y = df[df.columns[i]].to_list()
            scatter = Scatter(x=x, y=y, name=df.columns[i], **scatter_options)

            in_column = df.columns[i] == variable_state.representation
            if variable_state and in_column:
                y_reference = df[df.columns[1]]
                scatter_reference = Scatter(
                    x=x,
                    y=y_reference,
                    name=df.columns[1],
                    **scatter_options
                )
                fig.add_trace(scatter_reference)
                main_figure.add_trace(scatter_reference)

            fig.update_xaxes(rangeslider_visible=True)
            fig.update_yaxes(autorange=True, fixedrange=False)
            fig.update_layout(hovermode='x unified', template="seaborn")

            figures.append(fig.add_trace(scatter))
            main_figure.add_trace(scatter)

        main_figure.update_xaxes(rangeslider_visible=True)
        main_figure.update_yaxes(autorange=True, fixedrange=False)
        main_figure.update_layout(hovermode='x unified', template="seaborn")
        figures.append(main_figure)

        return figures
