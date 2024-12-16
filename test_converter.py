import pytest
from currency_converter import fetch_exchange_rate, convert_currency

# Mock API Key for testing
VALID_API_KEY = "82b5aa51b9de0f1abd6e7a8a"
INVALID_API_KEY = "INVALID_API_KEY"

# Test fetch_exchange_rate

def test_fetch_exchange_rate_success():
    """Тест успешного получения курса валют."""
    rate = fetch_exchange_rate("USD", "EUR", VALID_API_KEY)
    assert rate > 0, "Курс валют должен быть положительным"

def test_fetch_exchange_rate_invalid_key():
    """Тест с неверным API-ключом."""
    with pytest.raises(Exception):
        fetch_exchange_rate("USD", "EUR", INVALID_API_KEY)

def test_fetch_exchange_rate_invalid_currency():
    """Тест с неверным кодом валюты."""
    with pytest.raises(Exception):
        fetch_exchange_rate("INVALID", "EUR", VALID_API_KEY)

# Test convert_currency

def test_convert_currency_success():
    """Тест успешной конверсии валют."""
    result = convert_currency("USD", "EUR", 100, VALID_API_KEY)
    assert result["result"] > 0, "Результат конверсии должен быть положительным"
    assert result["amount"] == 100, "Сумма должна соответствовать входному значению"
    assert result["base_currency"] == "USD", "Исходная валюта должна совпадать"
    assert result["target_currency"] == "EUR", "Целевая валюта должна совпадать"

def test_convert_currency_negative_amount():
    """Тест с отрицательной суммой."""
    with pytest.raises(ValueError):
        convert_currency("USD", "EUR", -100, VALID_API_KEY)

def test_convert_currency_zero_amount():
    """Тест с нулевой суммой."""
    with pytest.raises(ValueError):
        convert_currency("USD", "EUR", 0, VALID_API_KEY)

def test_convert_currency_invalid_currency():
    """Тест с неверным кодом валюты."""
    with pytest.raises(Exception):
        convert_currency("INVALID", "EUR", 100, VALID_API_KEY)

# Run tests with pytest
if __name__ == "__main__":
    pytest.main()
