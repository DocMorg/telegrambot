from app import app
from app import config
import telebot
from telebot import types
import time
# import httplib2
# import googleapiclient.discovery
# from oauth2client.service_account import ServiceAccountCredentials

# CREDENTIALS_FILE = 'woven-environs-272314-a2f4d17f757a.json'
# credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
# ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

# httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
# service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/{}'.format(secret), methods=["POST"])
def web_hook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    print("Message")
    return "ok", 200


@bot.message_handler(content_types=['text'])
def start_command(message):
    if message.text == "/start":
        keyboard = types.InlineKeyboardMarkup()
        callback_button_teacher = types.InlineKeyboardButton(text="Я преподаватель", callback_data="teacher")
        callback_button_student = types.InlineKeyboardButton(text="Я студент", callback_data="student")
        keyboard.add(callback_button_teacher)
        keyboard.add(callback_button_student)
        bot.send_message(message.chat.id, text='Выберите роль', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "teacher":
            # keyboard = types.InlineKeyboardMarkup()
            bot.send_message(chat_id=call.message.chat.id, text='Представьтесь, пожалуйста')
            bot.register_next_step_handler(message, teacher_name_step)
        elif call.data == "student":
            bot.send_message(chat_id=call.message.chat.id, text='Представьтесь, пожалуйста')
            bot.register_next_step_handler(message, student_name_step)


def teacher_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        teacher = Teacher_data(name)
        teacher_dict[chat_id] = teacher
        teacher_dict.teacher_id = chat_id
        msg = bot.send_message(chat_id, text='Введите ссылку на таблицу Google')
        bot.register_next_step_handler(msg, teacher_table_link_step)
    except Exception as e:
        bot.reply_to(message, "Не понял Вас")


def teacher_table_link_step(message):
    try:
        chat_id = message.chat.id
        link = message.text
        teacher = teacher_dict[chat_id]
        teacher.table_link = link
        msg = bot.send_message(chat_id, text='Введите, как таблица будет называться в боте')
        bot.register_next_step_handler(msg, teacher_table_name_step)
    except Exception as e:
        bot.reply_to(message, 'Не понял Вас')


def teacher_table_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        teacher = teacher_dict[chat_id]
        teacher.table_name = name
        msg = bot.send_message(chat_id, text='Принято')
    except Exception as e:
        bot.reply_to(message, 'Не понял Вас')


def student_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        student = Student_data(name)
        student_dict[chat_id] = student
        student_dict.student_id = chat_id
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add('')
        msg = bot.send_message(chat_id, text='Хотите передать свой номер телефона?')
        bot.register_next_step_handler(msg, student_phone_step)
    except Exception as e:
        bot.reply_to(message, 'Не понял Вас')

# def student_phone_step(message):
#     try:
#         chat_id = message.chat.id
#         keyboard =