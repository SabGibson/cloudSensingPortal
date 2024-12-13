import plotly.express as px
import plotly.graph_objects as go


def plot_min_values(df):
    fig = go.Figure()
    for col in df.columns:
        is_min = df[col] == df.min(axis=1)

        fig.add_trace(
            go.Scatter(
                x=df.index[is_min],
                y=df[col][is_min],
                name=f'Buy {col.split("_")[0].upper()}',
                mode="markers",
                marker=dict(size=10),
            )
        )

    fig.update_layout(
        title="Buy-No-Buy Showing Best Value Best Selling Items on Regional Amazon",
        xaxis_title="Time",
        yaxis_title="Value",
    )

    return fig
