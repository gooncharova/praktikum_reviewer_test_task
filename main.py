import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # условие в таком виде читается с трудом, необходимо переделать, расставив правильные переносы
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # нехорошо, что название переменной совпадает с названием класса выше
        # да и вообще нехорошо писать с большой буквы, лучше с маленькой
        for Record in self.records:
            # лучше вынести сегодняшнюю дату в отдельную переменную
            if Record.date == dt.datetime.now().date():
                # лучше использовать способ для суммирования, как ниже (формата x+=y)
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # все вычисления из условий нужно вынести в отдельные переменные
            # условие в таком виде читается с трудом
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # название переменных должно быть осмысленным
        x = self.limit - self.get_today_stats()
        if x > 0:
            # переносы строк должны быть без бэкслешей
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # здесь можно без else, просто return
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # не обязательно добавлять курсы валют в переменные метода, их можно вызвать через self
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        # более наглядно будет, если добавить курс рубля также в переменные класса
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        # не хватает пустой строки для логического разделения операций
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # переносы строк должны быть без бэкслешей
            # нужно использовать одинаковый способ форматирования строк, предпочтительно f-строки
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    def get_week_stats(self):
        super().get_week_stats()
