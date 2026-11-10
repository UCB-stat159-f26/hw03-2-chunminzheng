import pytest
import pandas as pd

from tenniscareer.data import (
    _normalize_name,
    _parse_career_js,
    _process_matches,
    _calculate_age,
    _add_opponent_age,
    _detect_gender,
)

def test_normalize_name():
    assert _normalize_name("serena williams") == "SerenaWilliams"
    assert _normalize_name("Serena Williams") == "SerenaWilliams"
    assert _normalize_name("SerenaWilliams") == "SerenaWilliams"


def test_empty_name():
    with pytest.raises(ValueError, match="cannot be empty"):
        _normalize_name("")


def test_parse_career_js():
    mock_js = (
        'var morematchmx = [["19951030", "Canadian Open", '
        '"Carpet", "W", "L"]];'
    )
    matches = _parse_career_js(mock_js)

    assert len(matches) == 1
    assert matches[0][0] == "19951030"
    assert matches[0][4] == "L"


def test_invalid_js():
    with pytest.raises(ValueError, match="match records not found"):
        _parse_career_js("invalid JavaScript")

def test_female_opponent_age():
    mock_js = (
        'var morematchmx = [["19951030", "Canadian Open", '
        '"Carpet", "W", "L", "", "", "WC", "Q1", '
        '"6-1 6-1", "3", "Anne Miller", "149", "7", '
        '"", "R", "19770119"]];'
    )
    df = _process_matches(_parse_career_js(mock_js))

    assert _detect_gender(df) == "female"
    df = _add_opponent_age(df, "female")

    assert df.loc[0, "opponent"] == "Anne Miller"
    assert df.loc[0, "opponent_age"] == pytest.approx(18.776, abs=0.01)


def test_male_opponent_age():
    mock_js = (
        'var morematchmx = [["20010910", "Spain F10", '
        '"Hard", "S", "L", "", "", "WC", "R32", '
        '"2-6 7-5 6-2", "3", "Guillermo Platel", "731", '
        '"", "", "R", "22.264202601"]];'
    )
    df = _process_matches(_parse_career_js(mock_js))

    assert _detect_gender(df) == "male"
    df = _add_opponent_age(df, "male")

    assert df.loc[0, "opponent"] == "Guillermo Platel"
    assert df.loc[0, "opponent_age"] == pytest.approx(22.2642)

def test_female_missing_opponent_age():
    df = pd.DataFrame({
        "date": pd.to_datetime(["1995-10-30", "1997-03-07"]),
        "opponent_age_raw": ["19770119", ""]
    })

    result = _add_opponent_age(df, "female")

    assert result["opponent_age"].notna().iloc[0]
    assert pd.isna(result["opponent_age"].iloc[1])

def test_male_missing_opponent_age():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2001-09-10", "2001-09-17"]),
        "opponent_age_raw": ["22.264202601", ""]
    })

    result = _add_opponent_age(df, "male")

    assert result["opponent_age"].iloc[0] == pytest.approx(22.2642)
    assert pd.isna(result["opponent_age"].iloc[1])

def test_detect_gender_with_missing_values():
    female_df = pd.DataFrame({
        "opponent_age_raw": ["", "19770119", "19700503"]
    })

    male_df = pd.DataFrame({
        "opponent_age_raw": ["", "22.264202601", "24.2902121834"]
    })

    assert _detect_gender(female_df) == "female"
    assert _detect_gender(male_df) == "male"

def test_detect_gender_all_missing():
    df = pd.DataFrame({
        "opponent_age_raw": ["", None, ""]
    })

    with pytest.raises(ValueError, match="Cannot determine"):
        _detect_gender(df)
