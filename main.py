import telebot
from telebot import types
from config import TG_TOKEN #import from confif.py, where is the bot token located

token = TG_TOKEN
bot = telebot.TeleBot(token)

adm = #chat_id

markup_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_start.add(*[types.KeyboardButton(name) for name in ['Отзыв', 'Вопрос']])
markup_start.add(*[types.KeyboardButton(name) for name in ['Предложение']])

markup_cancel = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_cancel.add(types.KeyboardButton("Отмена"))

@bot.message_handler(commands=['start'])
def start_message(message):

    bot.send_message(message.chat.id, "Привет. Выбери, что ты хочешь отправить", reply_markup=markup_start)
    bot.send_photo(message.chat.id, 'https://i.imgur.com/3pVINt0.png', 'Чтобы Админ смог вам ответить - измените настройки приватности: Пересылка сообщений - все.')

def forward_adm_fb(message):

    if message.text.lower() == 'отмена':
        bot.send_message(message.chat.id, "Возвращаемся назад...", reply_markup=markup_start)
    else:
        print('->forward_adm_fb')
        print('User text to admin')
        print(f'{message.chat.id} - User -> {adm} - Admin, text = {message.text}'), print()

        msg = bot.forward_message(adm, message.chat.id, message.message_id)
        bot.reply_to(msg,"🟢 Отзыв")
        bot.send_message(message.chat.id, "Сообщение было отправлено! Выбери, что ты хочешь отправить", reply_markup=markup_start)

def forward_adm_qs(message):

    if message.text.lower() == 'отмена':
        bot.send_message(message.chat.id, "Возвращаемся назад...", reply_markup=markup_start)
    else:
        print('->forward_adm_qs')
        print('User text to admin')
        print(f'{message.chat.id} - User -> {adm} - Admin, text = {message.text}'), print()

        msg = bot.forward_message(adm, message.chat.id, message.message_id)
        bot.reply_to(msg,"🟡 Вопрос")
        bot.send_message(message.chat.id, "Сообщение было отправлено! Выбери, что ты хочешь отправить", reply_markup=markup_start)

def forward_adm_sg(message):

    if message.text.lower() == 'отмена':
        bot.send_message(message.chat.id, "Возвращаемся назад...", reply_markup=markup_start)
    else:
        print('->forward_adm_sg')
        print('User text to admin')
        print(f'{message.chat.id} - User -> {adm} - Admin, text = {message.text}'), print()

        msg = bot.forward_message(adm, message.chat.id, message.message_id)
        bot.reply_to(msg,"🔴 Предложение")
        bot.send_message(message.chat.id, "Сообщение было отправлено! Выбери, что ты хочешь отправить", reply_markup=markup_start)

@bot.message_handler(content_types=['text'])
def message(message):

    # если пишет Админ
    if message.chat.id == adm:
        reply = message.reply_to_message
        if reply:
            if reply.forward_from != None:

                print('->forward_usr')
                print('Admin text to user')
                print(f'{adm} - Admin -> {reply.forward_from.id} - User, text = {message.text}'), print()

                text = 'Сообщение от автора:\n' + message.text

                bot.send_message(
                    chat_id=reply.forward_from.id,
                    text = text
                )
            else:
                bot.send_message(
                    chat_id=adm,
                    text="Аккаунт пользователя - приватный"
                )
                print('->forward_usr')
                print('Admin text to user')
                print('Error. User\'s account is private'), print()

        else:
            bot.send_message(adm, 'Сделайте reply сообщение, чтобы ответить пользователю')

    # если пишет Пользователь
    else:
        if message.text.lower() == 'отзыв':

            msg = bot.send_message(message.chat.id, 'Напиши свой отзыв', reply_markup=markup_cancel)
            bot.register_next_step_handler(msg, forward_adm_fb)

        elif message.text.lower() == 'вопрос':

            msg = bot.send_message(message.chat.id, 'Напиши свой вопрос', reply_markup=markup_cancel)
            bot.register_next_step_handler(msg, forward_adm_qs)

        elif message.text.lower() == 'предложение':

            msg = bot.send_message(message.chat.id, 'Напиши свое предложение', reply_markup=markup_cancel)
            bot.register_next_step_handler(msg, forward_adm_sg)


def main():
    print('Bot is activated')
    bot.infinity_polling()


if __name__ == "__main__":
    main()
