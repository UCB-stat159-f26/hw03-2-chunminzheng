import matplotlib.pyplot as plt

def plot_player_career(df):
    """Plot player age against age difference for career matches."""
    required = {"player_age", "age_difference", "result"}

    if not required.issubset(df.columns):
        raise ValueError("DataFrame is missing required columns.")

    fig, ax = plt.subplots(figsize=(10, 6))

    colors = {"W": "steelblue", "L": "tomato"}

    for result, color in colors.items():
        subset = df[df["result"] == result]
        ax.scatter(subset["player_age"], subset["age_difference"],
                   c=color, alpha=0.5, s=12, label=result)

    ax.axhline(0, color="gray", linestyle="--", linewidth=1)
    ax.set_xlabel("Player Age (years)")
    ax.set_ylabel("Player Age - Opponent Age (years)")
    ax.set_title("Career Matches by Age Difference")
    ax.legend(title="Result")
    return fig
