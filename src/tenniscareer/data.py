import requests
import json
import pandas as pd
import re

def _normalize_name(player_name):
    """Convert a player's name into Tennis Abstract URL format."""
    if not isinstance(player_name, str):
        raise ValueError("Player name must be a string.")

    name = player_name.strip()

    if not name:
        raise ValueError("Player name cannot be empty.")

    if " " in name:
        return "".join(word.capitalize() for word in name.split())

    return name[0].upper() + name[1:]

def _fetch_career_js(player_name):
    """Download a player's career match JavaScript file."""
    name = _normalize_name(player_name)
    url = f"https://www.tennisabstract.com/jsmatches/{name}Career.js"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as error:
        raise ValueError(
            f"Could not retrieve career data for '{player_name}'."
        ) from error

    return response.text

def _parse_career_js(js_text):
    """Extract match records from Tennis Abstract JavaScript."""
    marker = "var morematchmx ="

    if marker not in js_text:
        raise ValueError("Invalid career JS data: match records not found.")

    data = js_text.split(marker, 1)[1].strip()
    data = data.split(";", 1)[0].strip()

    try:
        matches = json.loads(data)
    except json.JSONDecodeError as error:
        raise ValueError("Unable to parse career match data.") from error

    return matches

def _process_matches(matches):
    """Convert raw match records into a DataFrame."""
    records = []

    for match in matches:
        records.append({
            "date": match[0],
            "result": match[4],
            "opponent": match[11],
            "opponent_age_raw": match[16]
        })

    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    return df

def _calculate_age(birth_date, match_dates):
    """Calculate age in years on each match date."""
    birth_date = pd.to_datetime(birth_date, format="%Y%m%d")
    return (match_dates - birth_date).dt.days / 365.25

def _add_opponent_age(df, gender):
    """Calculate opponent ages for female or male match data."""
    df = df.copy()

    if gender == "female":
        dob = pd.to_datetime(
            df["opponent_age_raw"], format="%Y%m%d", errors="coerce"
        )
        df["opponent_age"] = (df["date"] - dob).dt.days / 365.25
    elif gender == "male":
        df["opponent_age"] = pd.to_numeric(
            df["opponent_age_raw"], errors="coerce"
        )
    else:
        raise ValueError("Gender must be 'female' or 'male'.")

    return df

def get_player_matches(player_name):
    """Retrieve and process a player's career match data."""
    js_text = _fetch_career_js(player_name)
    matches = _parse_career_js(js_text)
    df = _process_matches(matches)

    birth_date = _fetch_player_birthdate(player_name)
    gender = _detect_gender(df)

    df["player_age"] = _calculate_age(birth_date, df["date"])
    df = _add_opponent_age(df, gender)
    df["age_difference"] = df["player_age"] - df["opponent_age"]

    return df

def _fetch_player_birthdate(player_name):
    """Retrieve a player's date of birth from Tennis Abstract."""
    name = _normalize_name(player_name)
    url = f"https://www.tennisabstract.com/jsmatches/{name}.js"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as error:
        raise ValueError(
            f"Could not retrieve player information for '{player_name}'."
        ) from error

    match = re.search(r"\bvar\s+dob\s*=\s*['\"]?(\d{8})", response.text)

    if not match:
        raise ValueError(f"Birth date not found for '{player_name}'.")

    return match.group(1)

def _detect_gender(df):
    """Detect the match data format from opponent age values."""
    values = df["opponent_age_raw"].dropna().astype(str)
    values = values[values.str.strip() != ""]

    if values.empty:
        raise ValueError("Cannot determine player data format.")

    sample = values.iloc[0]

    if len(sample) == 8 and sample.isdigit():
        return "female"

    return "male"
