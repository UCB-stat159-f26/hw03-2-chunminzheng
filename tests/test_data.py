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
