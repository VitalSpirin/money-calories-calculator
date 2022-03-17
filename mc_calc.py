# Проект: Спринт 2. Калькуляторы денег и калорий.
import datetime as dt
from typing import Dict, List, Optional, Tuple

LOCAL_DATE_FORMAT: str = "%d.%m.%Y"


class Record:
    """Функциональность для удобного создания записей."""

    def __init__(
        self, amount: float, comment: str, date: Optional[str] = None
    ) -> None:
        self.amount: float = amount
        self.comment: str = comment
        self.date: dt.date
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, LOCAL_DATE_FORMAT).date()


class Calculator:
    """Функциональность обеих калькуляторов."""

    def __init__(self, limit: int) -> None:
        self.limit: int = limit
        self.records: List[Record] = []

    def add_record(self, record: Record) -> None:
        """Сохранить новую запись о расходах/приёме пищи."""
        self.records.append(record)

    def get_today_balance(self) -> float:
        """Получить данные о балансе/доступных калориях на текущий момент."""
        return self.limit - self.get_today_stats()

    def get_today_stats(self) -> float:
        """Посчитать, сколько денег/калорий потрачено/уже съедено сегодня."""
        today: dt.date = dt.date.today()
        return sum(x.amount for x in self.records if x.date == today)

    def get_week_stats(self) -> float:
        """
        Посчитать, сколько денег/калорий
        потрачено/получено за последние 7 дней.
        """
        today: dt.date = dt.date.today()
        week_ago: dt.date = today - dt.timedelta(days=7)

        return sum(
            x.amount for x in self.records if week_ago < x.date <= today
        )


class CaloriesCalculator(Calculator):
    """Функциональность калькулятора калорий."""

    def get_calories_remained(self) -> str:
        """Определить, сколько ещё калорий можно/нужно получить сегодня."""
        today_balance: float = self.get_today_balance()
        if today_balance > 0:
            return (
                "Сегодня можно съесть что-нибудь ещё, "
                "но с общей калорийностью не более "
                f"{today_balance} кКал"
            )
        return "Хватит есть!"


class CashCalculator(Calculator):
    """Функциональность калькулятора денег."""

    RUB_RATE: float = 1.0
    USD_RATE: float = 104.80
    EURO_RATE: float = 115.93

    def get_today_cash_remained(self, currency: str) -> str:
        """
        Определить, сколько ещё денег можно потратить
        сегодня в рублях, долларах или евро.
        """
        today_cash: float = self.get_today_balance()

        if today_cash == 0:
            return "Денег нет, держись"

        currency_attrib: Dict[str, Tuple[str, float]]
        currency_attrib = {
            "rub": ("руб", self.RUB_RATE),
            "usd": ("USD", self.USD_RATE),
            "eur": ("Euro", self.EURO_RATE),
        }

        if currency not in currency_attrib:
            return (
                f"Тип валюты {currency} неизвестен. "
                "Корректный расчёт невозможен."
            )

        currency_name: str
        currency_rate: float
        currency_name, currency_rate = currency_attrib[currency]

        cash_in_currency: float = round(today_cash / currency_rate, 2)

        if cash_in_currency < 0:
            today_debt: float = abs(cash_in_currency)
            return (
                "Денег нет, держись: твой долг - "
                f"{today_debt} {currency_name}"
            )

        return f"На сегодня осталось {cash_in_currency} {currency_name}"
