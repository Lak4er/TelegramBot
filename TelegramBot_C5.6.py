
import telebot
from extensions import keys, CryptoConverter, APIException
from TOKEN import TOKEN
from telebot import types

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help','info'])
def help(message: telebot.types.Message):
    text = f"Привет {message.from_user.username}\n" \
           f"Чтобы начать работу с ботом, вводите команды в следующем формате:\n " \
           "<имя валюты>" \
           "<в какую валюту перевести>" \
           "<количество переводимой валюты>\n" \
           "Например:\n" \
           "биткоин доллар 100"
    bot.reply_to(message, text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    Help = types.KeyboardButton(" 🆘 Помощь")
    Values = types.KeyboardButton("💵💴💶💷 Доступные валюты")
    markup.add(Help, Values)
    bot.send_message(message.chat.id, "Для удобства воспользуйтесь кнопками", reply_markup=markup)

@bot.message_handler (commands = ['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler (content_types = ['text', ])
def convert(message: telebot.types.Message):
    if message.text == "💵💴💶💷 Доступные валюты":
        text = "Список валют:"
        for key in keys.keys():
            text = "\n".join((text, key,))
        bot.reply_to(message, text)
    elif message.text == "🆘 Помощь":
        text = "Чтобы начать работу с ботом, вводите команды в следующем формате:\n " \
           "<имя валюты>" \
           "<в какую валюту перевести>" \
           "<количество переводимой валюты>\n" \
           "Например:\n" \
           "биткоин доллар 100"
        bot.reply_to(message, text)
    else:
        try:
            values = message.text.split(" ")

            if len(values) != 3:
                raise APIException("Параметров должно быть три!!!\n для вызова кнопочек пропишите /info")

            quote, base, amount = values
            total_base = CryptoConverter.get_price(quote, base, amount)
        except APIException as e:
            bot.reply_to(message, f'Ошибка пользователя\n{e}\n для вызова кнопочек пропишите /info')
        except Exception as e:
            bot.reply_to(message, f'Не удалось обработать команду\n{e}\n для вызова кнопочек пропишите /info')
        else:
            text = f'Цена {amount} {quote} {keys[quote]} в {base} составит {total_base} {keys[base]}'
            bot.send_message(message.chat.id, text)

bot.polling(none_stop = True)
