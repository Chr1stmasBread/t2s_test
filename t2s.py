import requests
import telebot
from GPT_token import *

# Токен вашего бота от BotFather
TOKEN = '7062249945:AAHmQumUDijnWEFXe8pGqGNc8gp3NwqYk3M'

# IAM-токен и ID папки для доступа к Yandex SpeechKit
IAM_TOKEN = f'{iam_token}'
FOLDER_ID = 'b1gh7qec08g3hugo7d7g'

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Обработка команды /start
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я Text-to-Speech бот на Python.\n Напиши команду /tts и текст, который Вы хотите конвертировать в голосовой формат. Я отправлю Вам готовую работу.")

# Функция для обработки команды /tts
@bot.message_handler(commands=['tts'])
def request_text(message):
    bot.send_message(message.chat.id, "Я готов к работе с вашим текстом. Пожалуйста, отправьте текст для озвучки.")

# Функция для обработки текстовых сообщений после команды /tts
@bot.message_handler(func=lambda message: True, content_types=['text'])
def text_to_speech(message):
    # Отправляем "набирает сообщение" в чат
    bot.send_chat_action(message.chat.id, 'typing')

    # Получаем текст из сообщения пользователя
    text = message.text

    # Параметры запроса к SpeechKit
    data = {
        'text': text,
        'speed': 1.1,  # Скорость речи
        'emotion': 'good',  # Эмоциональная окраска
        'lang': 'ru-RU',  # Язык текста (русский)
        'voice': 'jane',  # Голос Джейн
        'folderId': FOLDER_ID,
    }
    headers = {'Authorization': f'Bearer {IAM_TOKEN}'}

    # Отправка запроса к SpeechKit
    response = requests.post('https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize', headers=headers, data=data)

    # Обработка ответа
    if response.status_code == 200:
        # Отправка аудиосообщения пользователю
        bot.send_voice(message.chat.id, response.content)
    else:
        # Сообщение об ошибке, если запрос к SpeechKit завершился неудачно
        bot.reply_to(message, "При преобразовании текста в речь возникла ошибка")

# Запуск бота
bot.polling()