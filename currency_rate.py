from requests import get, utils


def currency_rate(money, currency='USD'):
    currency = currency.upper()
    response = get('https://www.cbr.ru/scripts/XML_daily.asp')
    endcodings = utils.get_encoding_from_headers(response.headers)
    content = response.content.decode(encoding=endcodings)
    if currency not in content:
        print('None')
    else:
        currency_date = content[content.find('Date') + 6: ((content.find('Date')) + 16):]
        # print(currency_date)
        slice_val = (
        content[content.find(currency): ((content.find(currency)) + 85):])
        value = slice_val.replace('</', ' ').replace('>', ' ').replace(',',
                                                                       '.').replace(
            '<', ' ').split()

        kurs = []
        for val in value:
            if val.isalpha() != True:
                kurs.append(val)
        kurs[1] = float(kurs[1])
        # print('Курс :', (kurs[0]), (currency), ' = ',
        #       "{0:.2f} RUB".format(kurs[1]))
        # print(value)

        return f'{(money * kurs[1]): .{2}f}'


if __name__ == '__main__':
    from sys import argv
    # print(currency_rate(10))
    currency_rate(argv[1])
