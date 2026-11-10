import pytest
import pandas as pd
import matplotlib

matplotlib.use("Agg")

from matplotlib.figure import Figure
from tenniscareer.plotting import plot_player_career

def test_plot_player_career():
    df = pd.DataFrame({
        "player_age": [20, 21, 22, 23],
        "age_difference": [-3, 2, -1, 4],
        "result": ["W", "L", "W", "L"]
    })

    fig = plot_player_career(df)

    assert isinstance(fig, Figure)
    assert fig.axes[0].get_xlabel() == "Player Age (years)"
    assert fig.axes[0].get_ylabel() == "Player Age - Opponent Age (years)"

def test_plot_missing_columns():
    df = pd.DataFrame({"player_age": [20, 21]})

    with pytest.raises(ValueError, match="missing required columns"):
        plot_player_career(df)
