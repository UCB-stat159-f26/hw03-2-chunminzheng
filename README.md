# tenniscareer

This is a Python package I created for STAT 159 Homework 3 at UC Berkeley. It uses match data from [Tennis Abstract](https://www.tennisabstract.com/) to explore how tennis players' ages compare with their opponents throughout their careers.

The package builds on my work from HW1 and HW2. Instead of running separate scripts for downloading, cleaning, and plotting data, I combined these steps into a package that can be used for different tennis players.

## Features

The package has two main functions:

- `get_player_matches()`: Downloads and processes a player's career match data from Tennis Abstract. It calculates the player's age, the opponent's age, and the difference between their ages.
- `plot_player_career()`: Creates a scatter plot showing the age difference between a player and their opponents throughout their career, with different colors for wins and losses.

The package supports both men's and women's match data. It also handles different name formats, such as `"Serena Williams"`, `"serena williams"`, and `"SerenaWilliams"`.

## Installation

You can install the package directly from GitHub using:

```bash
pip install git+https://github.com/UCB-stat159-f26/hw03-2-chunminzheng.git
```

The required Python dependencies will be installed automatically.

## Usage

First, import the two main functions:

```python
from tenniscareer import get_player_matches, plot_player_career
import matplotlib.pyplot as plt
```

### Example 1: Serena Williams

```python
serena = get_player_matches("Serena Williams")

print(serena.head())

plot_player_career(serena)
plt.show()
```

### Example 2: Rafael Nadal

```python
rafa = get_player_matches("Rafael Nadal")

print(rafa.head())

plot_player_career(rafa)
plt.show()
```

### Invalid Player Name

If a player cannot be found, the function raises a `ValueError` with an error message.

For example:

```python
get_player_matches("GastonSanchez")
```

This produces an error indicating that the player's career data could not be retrieved.

## Data and Visualization

The data comes from Tennis Abstract's player career JavaScript files.

The cleaned DataFrame contains the match date, result, opponent's name, player's age, opponent's age, and age difference.

The scatter plot uses:

- **X-axis:** Player's age at the time of each match.
- **Y-axis:** Player's age minus opponent's age.
- **Blue points:** Wins.
- **Red points:** Losses.

A positive age difference means the player was older than their opponent, while a negative difference means the player was younger.

The plot does not include annotations.

## Testing

I used `pytest` to test the package.

The automated tests use mock match data instead of downloading data from the live Tennis Abstract website. This makes the tests more reliable and allows them to run without an internet connection.

To install pytest:

```bash
pip install pytest
```

To run the tests from the repository directory:

```bash
python -m pytest -v
```

The tests check name formatting, JavaScript parsing, men's and women's opponent age calculations, plot creation, and error handling.

## Personal Reflections

One thing I learned from this assignment was how to turn code from previous homework assignments into a Python package. In HW2, I had separate scripts for downloading, cleaning, and plotting the tennis data. For HW3, I had to reorganize that code into functions that could work for different players instead of just Serena Williams.

One of the more challenging parts was figuring out how Tennis Abstract stores its data. I found out that the men's and women's match files use different formats for opponent ages, so I had to handle them differently. I also spent some time figuring out where the website stores each player's birth date. This helped me get more comfortable with reading JavaScript data and debugging code when something did not work as expected.

I also learned more about writing tests with `pytest`. Before this assignment, I mostly checked whether my code worked by running it myself. Using mock data showed me how to test specific parts of my code without relying on a website.

Overall, this assignment helped me understand Python packages, testing, and code organization better. I also got more practice using Git and GitHub to keep track of changes throughout the project.
