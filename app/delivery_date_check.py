import run
from datetime import date


def check_date():
    d = date.today().strftime("%Y.%m.%d")
    data = run.get_data()
    result = []
    for i in data:
        delivery_date = i[4].split('.')[::-1]
        string = '.'.join(delivery_date)
        if d < string:
            pass
        else:
            _ = [f'У заказа № {i[2]} прошел срок поставки ({i[4]})']
            result = result + _
    return result


if __name__ == "__main__":
    check_date()
