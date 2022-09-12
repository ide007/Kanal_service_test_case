"""
Данный модуль случит для получения курса валюты с сайта Центра Банка
https://www.cbr.ru на текущую дату.
"""
from requests import get, utils


def currency_rate(currency='USD'):
    """Функция для получения рублевого эквивалента иностранной валюты.
    :param currency: валюта(3 символа на латинской раскладке, в любом регистре)
    :return: номинал в российской валюте
    """

    currency = currency.upper() # валюта
    # api ЦБ для получения данных
    response = get('https://www.cbr.ru/scripts/XML_daily.asp')
    # определение кодировки
    endcode = utils.get_encoding_from_headers(response.headers)
    # декодирование сырых данных
    content = response.content.decode(encoding=endcode)
    if currency not in content:
        print('None')
    else:
        # currency_date = content[content.find('Date') + 6:
        # ((content.find('Date')) + 16):]
        # поиск нужной валюты
        slice_val = (
            content[content.find(currency): ((content.find(currency)) + 85):])
        # отчистка данных от мусора
        value = slice_val.replace('</', ' ').replace('>', ' ').replace(
            ',', '.').replace('<', ' ').split()

        exchange_rate = []
        for val in value:
            if not val.isalpha():
                exchange_rate.append(float(val))
        # print('Курс :', (exchange_rate[0]), (currency), ' = ',
        #       "{0:.2f} RUB".format(exchange_rate[1]))
        # print(value)

        return f'{(exchange_rate[1] / exchange_rate[0]):.{2}f}'


if __name__ == '__main__':
    # print(currency_rate(10000, 'uzs'))
    from sys import argv
    # при необходимости можно выбрать валюту через параметр argv
    currency_rate(argv[1])
