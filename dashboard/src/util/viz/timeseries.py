import plotly.graph_objects as go


def plot_timeseries_fx(df, exc_curr):
    fig = go.Figure()
    for col in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df[col], name=f"{col.split('_')[0].upper()} Curncy"
            )
        )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title=f"Exchange Rate per EUR",
        title=f"EUR{exc_curr.upper()} Exchange Rate vs Time",
    )

    return fig


def plot_timeseries_snapshot(df, curr, name):
    fig = go.Figure()
    for col in df.columns:
        fig.add_trace(
            go.Scatter(x=df.index, y=df[col], name=f"{col.split('_')[0].upper()}")
        )

    fig.update_layout(
        xaxis_title="Time",
        yaxis_title=f"Average Snapshot Value {curr.upper()}",
        title=f"Average Snapshot Value {name.upper()}",
    )

    return fig
