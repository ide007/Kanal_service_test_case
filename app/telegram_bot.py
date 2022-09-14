import telebot
from app.delivery_date_check import check_date

bot = telebot.TeleBot('5591075887:AAHqJoAHlBWctgVfVUXuDTUZbKw4-2h28rE')
check = check_date()


@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_message(message):
    if message.text == 'Привет':
        bot.send_message(message.from_user.id, 'Здравствуйте! чем могу помочь?')
    elif message.text == '/help':
        bot.send_message(message.from_user.id, 'напиши /check')
    elif message.text == '/check':
        for i in check:
            bot.send_message(message.from_user.id, f'{i}')
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю. Напиши /help.')


def main():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
