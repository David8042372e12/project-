import tkinter as tk
from tkinter import messagebox
import requests
import argparse
import json
from datetime import datetime

# BEGIN: Helper Functions
def fetch_exchange_rate(base_currency, target_currency, api_key):
    """
    Получить курс валют через API.

    Args:
        base_currency (str): Код исходной валюты.
        target_currency (str): Код целевой валюты.
        api_key (str): API-ключ.

    Returns:
        float: Курс обмена.

    Raises:
        Exception: Если запрос завершился неудачей.
    """
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["result"] == "success":
            return data["conversion_rate"]
        else:
            raise ValueError("Ошибка получения курса валют.")
    except Exception as e:
        raise Exception(f"Ошибка при запросе данных: {e}")


def convert_currency(base_currency, target_currency, amount, api_key):
    """
    Конвертировать сумму из одной валюты в другую.

    Args:
        base_currency (str): Исходная валюта.
        target_currency (str): Целевая валюта.
        amount (float): Сумма для конвертации.
        api_key (str): API-ключ.

    Returns:
        dict: Результаты конверсии, включая курс, результат и временную метку.
    """
    rate = fetch_exchange_rate(base_currency, target_currency, api_key)
    result = amount * rate
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "timestamp": timestamp,
        "base_currency": base_currency,
        "target_currency": target_currency,
        "amount": amount,
        "rate": rate,
        "result": result,
    }


def save_conversion_history(history, output_path):
    """
    Сохранить историю конверсий в файл JSON.

    Args:
        history (list): История конверсий.
        output_path (str): Путь к файлу для сохранения.
    """
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)

# END: Helper Functions

# Создание интерфейса приложения
root = tk.Tk()
root.title("Конвертер валют")
root.geometry("400x400")

# Глобальные переменные
conversion_history = []
api_key = "82b5aa51b9de0f1abd6e7a8a"  # Используется для тестов, заменить на свой API-ключ
output_file = "history.json"

# Интерфейс выбора валюты и ввода данных
base_currency_var = tk.StringVar(value="USD")
target_currency_var = tk.StringVar(value="EUR")

tk.Label(root, text="Выберите исходную валюту:").pack(pady=5)
base_currency_menu = tk.OptionMenu(root, base_currency_var, "USD", "EUR", "UAH", "RUB", "GBP")
base_currency_menu.pack(pady=5)

tk.Label(root, text="Выберите целевую валюту:").pack(pady=5)
target_currency_menu = tk.OptionMenu(root, target_currency_var, "USD", "EUR", "UAH", "RUB", "GBP")
target_currency_menu.pack(pady=5)

tk.Label(root, text="Введите сумму:").pack(pady=5)
amount_entry = tk.Entry(root)
amount_entry.pack(pady=5)

# Вывод результатов и управление
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Функции для кнопок

def on_convert():
    """Обработчик для кнопки конвертации."""
    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            raise ValueError("Сумма должна быть больше нуля.")
        result = convert_currency(base_currency_var.get(), target_currency_var.get(), amount, api_key)
        conversion_history.append(result)
        result_label.config(
            text=f"Результат: {result['amount']} {result['base_currency']} = {result['result']:.2f} {result['target_currency']}"
        )
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

def on_show_history():
    """Показать историю конверсий в отдельном окне."""
    if not conversion_history:
        messagebox.showinfo("История", "История конвертаций пуста.")
        return
    history_window = tk.Toplevel(root)
    history_window.title("История конвертаций")
    history_window.geometry("400x300")
    for i, entry in enumerate(conversion_history, 1):
        record = (
            f"{i}. {entry['timestamp']}:\n"
            f"{entry['amount']} {entry['base_currency']} → {entry['result']:.2f} {entry['target_currency']} "
            f"(Курс: {entry['rate']:.4f})\n"
        )
        tk.Label(history_window, text=record, anchor="w", justify="left").pack(fill="both", padx=10, pady=5)

def on_quit():
    """Закрыть приложение и сохранить историю."""
    save_conversion_history(conversion_history, output_file)
    root.destroy()

# Кнопки управления
convert_button = tk.Button(root, text="Конвертировать", command=on_convert)
convert_button.pack(pady=10)

menu_frame = tk.Frame(root)
menu_frame.pack(pady=20)

history_button = tk.Button(menu_frame, text="Показать историю", command=on_show_history)
history_button.grid(row=0, column=0, padx=10)

quit_button = tk.Button(menu_frame, text="Выход", command=on_quit)
quit_button.grid(row=0, column=1, padx=10)

root.mainloop()
