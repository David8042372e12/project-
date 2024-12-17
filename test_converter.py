import pytest
from currency_converter import fetch_exchange_rate, convert_currency, on_convert
import unittest
from unittest.mock import patch
from tkinter import Tk, StringVar, Entry, Label, messagebox

# Mock API Key for testing
VALID_API_KEY = "82b5aa51b9de0f1abd6e7a8a"
INVALID_API_KEY = "INVALID_API_KEY"



# Создаем заглушку для функции convert_currency
def mock_convert_currency(base_currency, target_currency, amount, api_key):
    return {"amount": amount, "base_currency": base_currency, "target_currency": target_currency, "result": 0.0}

# Обработчик для тестов
def on_convert_test(amount_entry, base_currency_var, target_currency_var, result_label, api_key):
    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            raise ValueError("Сумма должна быть больше нуля.")
        result = mock_convert_currency(base_currency_var.get(), target_currency_var.get(), amount, api_key)
        result_label.config(
            text=f"Результат: {result['amount']} {result['base_currency']} = {result['result']:.2f} {result['target_currency']}"
        )
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

class TestOnConvert(unittest.TestCase):
    def setUp(self):
        """Настройка тестового окружения"""
        self.root = Tk()
        self.amount_entry = Entry(self.root)
        self.base_currency_var = StringVar(value="USD")
        self.target_currency_var = StringVar(value="EUR")
        self.result_label = Label(self.root)
        self.api_key = "TEST_API_KEY"

    @patch("tkinter.messagebox.showerror")
    def test_zero_amount(self, mock_showerror):
        """Тест с нулевым значением суммы"""
        self.amount_entry.insert(0, "0")
        on_convert_test(self.amount_entry, self.base_currency_var, self.target_currency_var, self.result_label, self.api_key)
        mock_showerror.assert_called_once_with("Ошибка", "Сумма должна быть больше нуля.")

    @patch("tkinter.messagebox.showerror")
    def test_negative_amount(self, mock_showerror):
        """Тест с отрицательным значением суммы"""
        self.amount_entry.insert(0, "-50")
        on_convert_test(self.amount_entry, self.base_currency_var, self.target_currency_var, self.result_label, self.api_key)
        mock_showerror.assert_called_once_with("Ошибка", "Сумма должна быть больше нуля.")

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

def test_convert_currency_invalid_currency():
    """Тест с неверным кодом валюты."""
    with pytest.raises(Exception):
        convert_currency("INVALID", "EUR", 100, VALID_API_KEY)

# Run tests with pytest
if __name__ == "__main__":
    unittest.main()
    pytest.main()
